#!/usr/bin/env python3
"""$FRANC token creation via PumpPortal — thefranceway"""

import json, base64, requests, sys, os
from pathlib import Path
from datetime import datetime, timezone
from solders.keypair import Keypair
from solders.transaction import VersionedTransaction

# ── Token config ──
TOKEN_NAME        = "$FRANC"
TOKEN_TICKER      = "FRANC"
TOKEN_DESCRIPTION = (
    "$FRANC is the access token of thefranceway — a longevity and behavioral tech "
    "intelligence layer. Hold FRANC to unlock a token-gated AI agent, research swarm, "
    "and knowledge system at the intersection of human lifespan science, decentralized "
    "systems, and behavioral psychology. Built by Francesca Ranieri."
)
TOKEN_TWITTER  = ""   # add if desired
TOKEN_TELEGRAM = ""
TOKEN_WEBSITE  = "https://thefranceway.pages.dev"

WALLET_PATH    = os.path.expanduser("~/.config/solana/id.json")
ASSETS_DIR     = Path(__file__).parent.parent / "assets"
TOKEN_IMAGE    = ASSETS_DIR / "franc-token.png"

PUMPPORTAL_IPFS  = "https://pump.fun/api/ipfs"
PUMPPORTAL_TRADE = "https://pumpportal.fun/api/trade-local"
SOLANA_RPC       = "https://api.mainnet-beta.solana.com"

def load_keypair(path=WALLET_PATH):
    with open(path) as f:
        return Keypair.from_bytes(bytes(json.load(f)))

def upload_metadata(image_path):
    print(f"Uploading metadata from {image_path}...")
    with open(image_path, "rb") as img:
        files = {"file": ("franc-token.png", img, "image/png")}
        data  = {
            "name":        TOKEN_NAME,
            "symbol":      TOKEN_TICKER,
            "description": TOKEN_DESCRIPTION,
            "twitter":     TOKEN_TWITTER,
            "telegram":    TOKEN_TELEGRAM,
            "website":     TOKEN_WEBSITE,
            "showName":    "true",
        }
        r = requests.post(PUMPPORTAL_IPFS, files=files, data=data, timeout=30)
        r.raise_for_status()
    uri = r.json()["metadataUri"]
    print(f"Metadata URI: {uri}")
    return uri

def create_token(keypair, metadata_uri, dev_buy_sol=0.05):
    mint_keypair = Keypair()
    pub      = str(keypair.pubkey())
    mint_pub = str(mint_keypair.pubkey())

    print(f"Creating token with mint: {mint_pub}")

    payload = {
        "publicKey":     pub,
        "action":        "create",
        "tokenMetadata": {
            "name":   TOKEN_NAME,
            "symbol": TOKEN_TICKER,
            "uri":    metadata_uri,
        },
        "mint":             mint_pub,
        "denominatedInSol": "true",
        "amount":           dev_buy_sol,
        "slippage":         25,
        "priorityFee":      0.001,
        "pool":             "pump",
    }

    r = requests.post(PUMPPORTAL_TRADE, json=payload, timeout=30)
    r.raise_for_status()

    tx     = VersionedTransaction.from_bytes(r.content)
    signed = VersionedTransaction(tx.message, [keypair, mint_keypair])
    b64    = base64.b64encode(bytes(signed)).decode("ascii")

    result = requests.post(SOLANA_RPC, json={
        "jsonrpc": "2.0", "id": 1,
        "method":  "sendTransaction",
        "params":  [b64, {
            "encoding":             "base64",
            "skipPreflight":        False,
            "preflightCommitment":  "confirmed",
        }]
    }, timeout=30).json()

    if "error" in result:
        print(f"ERROR: {result['error']}")
        sys.exit(1)

    tx_sig = result["result"]

    info = {
        "name":         TOKEN_NAME,
        "ticker":       TOKEN_TICKER,
        "mint_address": mint_pub,
        "creator":      pub,
        "tx_signature": tx_sig,
        "metadata_uri": metadata_uri,
        "dev_buy_sol":  dev_buy_sol,
        "timestamp":    datetime.now(timezone.utc).isoformat(),
        "pump_fun_url": f"https://pump.fun/coin/{mint_pub}",
        "solscan_url":  f"https://solscan.io/tx/{tx_sig}",
    }

    info_path = ASSETS_DIR / "token-info.json"
    with open(info_path, "w") as f:
        json.dump(info, f, indent=2)

    print(f"\n$FRANC LAUNCHED!")
    print(f"  Mint:  {mint_pub}")
    print(f"  TX:    {tx_sig}")
    print(f"  URL:   https://pump.fun/coin/{mint_pub}")
    return info

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--dev-buy", type=float, default=0.05)
    parser.add_argument("--wallet",  default=WALLET_PATH)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not TOKEN_IMAGE.exists():
        print(f"ERROR: Token image not found at {TOKEN_IMAGE}")
        print("Place a 1000x1000 PNG at franc-token/assets/franc-token.png")
        sys.exit(1)

    kp = load_keypair(args.wallet)
    print(f"Wallet:   {kp.pubkey()}")

    # Check SOL balance
    bal_resp = requests.post(SOLANA_RPC, json={
        "jsonrpc": "2.0", "id": 1,
        "method": "getBalance", "params": [str(kp.pubkey())]
    }, timeout=15).json()
    sol_bal = bal_resp.get("result", {}).get("value", 0) / 1e9
    print(f"Balance:  {sol_bal:.4f} SOL")

    if sol_bal < args.dev_buy + 0.01:
        print(f"ERROR: Need at least {args.dev_buy + 0.01} SOL (have {sol_bal:.4f})")
        sys.exit(1)

    uri = upload_metadata(TOKEN_IMAGE)

    if args.dry_run:
        print("DRY RUN — stopping before token creation")
        sys.exit(0)

    create_token(kp, uri, args.dev_buy)
