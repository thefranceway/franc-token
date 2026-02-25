# $FRANC — Solana SPL Token

*by [@thefranceway](https://x.com/thefranceway)*
*Launched February 23, 2026*

---

## What Is $FRANC

$FRANC is a Solana SPL token launched as the community currency for the Agent-Human behavioral research project led by thefranceway.

This is my first token. I launched it to learn — and because the research needed a mechanism: airdrop $FRANC to participants in the behavioral study as a signal of participation and alignment.

---

## Token Details

| Field | Value |
|---|---|
| **Name** | $FRANC |
| **Ticker** | FRANC |
| **Chain** | Solana (SPL — standard, not Token-2022) |
| **Mint** | `BJ8MySahjvB3XFrKWxhFR4wsnjpgqY4gGRmU9wXHLCvu` |
| **Creator wallet** | `F65u1PZXx9FbD6TNnBBT2etgnfaBBUsuuLcHjri4HkN6` |
| **Launch platform** | pump.fun |
| **Launch TX** | `3D18bfjRL9sB7gZLqPKDPtQgP9wdZGw9BrD21u7PCiayB2MpY8VTjaxgzARSwtT5J8mz1eFVxykxBatNv6rqa73w` |
| **Status** | Bonding curve (graduation target: ~85 SOL) |

**Links:**
- [pump.fun](https://pump.fun/coin/BJ8MySahjvB3XFrKWxhFR4wsnjpgqY4gGRmU9wXHLCvu)
- [Solscan TX](https://solscan.io/tx/3D18bfjRL9sB7gZLqPKDPtQgP9wdZGw9BrD21u7PCiayB2MpY8VTjaxgzARSwtT5J8mz1eFVxykxBatNv6rqa73w)

---

## Why $FRANC Exists

The [Agent-Human Relationship Manual](https://github.com/thefranceway/agent-human-manual) is an ongoing behavioral study. Participants who complete the research questionnaire receive 50,000 $FRANC as an airdrop — a wallet-verifiable signal of participation.

$FRANC is also the bridge currency for a proposed cross-protocol interoperability model with $PAW (OpenPaw_PSM): hold $PAW → access FRANC tools, hold $FRANC → access PAW tools. Both projects are on standard SPL (not Token-2022) to avoid DeFi friction.

---

## What I Built and Learned

This repo contains the scripts I used to:

1. **Launch the token** (`launch/create-token.py`) — Using the PumpPortal API to create the SPL token, set metadata, upload to IPFS, and execute the launch transaction
2. **Generate the token image** (`make-image.py`) — Python/Pillow script to create the token visual
3. **Token metadata** (`assets/token-info.json`) — The on-chain record

**What I learned:**
- Standard SPL vs Token-2022: Token-2022 causes 48hr indexing delays on DEXes — use standard SPL for community tokens
- After bonding curve graduation, switch from PumpPortal to Jupiter Swap API (`lite-api.jup.ag/swap/v1`)
- IPFS metadata upload must happen before the launch transaction
- pump.fun bonding curve mechanics: ~85 SOL to graduate to Raydium

This is beginner work. It is documented here as a record of learning.

---

## Cross-Protocol: $FRANC × $PAW

**$PAW** (OpenPaw_PSM):
- CA: `DbukKVm7tdNaeaqjm8VD14TH4XMFEZ4xnjbXJ4SyEeLc`
- GitHub: [ExpertVagabond/paw-token](https://github.com/ExpertVagabond/paw-token)
- $PAW graduated pump.fun in 12 hours (~85 SOL) — confirms the graduation target

The cross-protocol model is being designed as a composable interoperability layer for community tokens in the agentic AI space.

---

## About

I am **thefranceway** — partnerships strategist and behavioral researcher. I study how humans and agents coordinate. $FRANC is the economic layer for that study.

I am not a developer. I launched this token by learning from documentation and doing. That is the point.

- X: [@thefranceway](https://x.com/thefranceway)
- Research: [Agent-Human Manual](https://github.com/thefranceway/agent-human-manual)
- Superteam: [earn.superteam.fun/t/thefranceway](https://earn.superteam.fun/t/thefranceway)
- Moltbook: thefranceway (m/humantech)

---

*First token. Learning in public. Documentation is the work.*
