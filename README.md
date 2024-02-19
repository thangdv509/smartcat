# SmartCat

SmartCat is a project from SmartLayer. Smart Cat represents a fully on-chain derivative of Cool Cat #2426.

This project run in Polygon blockchain network.

More information: https://www.smartlayer.network/smartcat

<img width="693" alt="Screenshot 2024-02-19 at 14 49 21" src="https://github.com/thangdv509/smartcat/assets/74363928/6313841b-21d3-41b2-aa16-e41bc720cb8c">

## What we need?

- Step 1: Setup _2_ metamask wallets
- Step 2: Buy the _same amount_ of smart cat for each wallet. Market: https://opensea.io/collection/smart-cat-reward
- Step 3: Adopt and name your cats at https://viewer.tokenscript.org/
- Step 4: Enjoy my tool

## Installion

From your command line:

```bash
# Install lighthouse globally
$ gitclone https://github.com/thangdv509/auto-tool-smartCat

# Install requirements
$ cd auto-tool-smartCat
$ pip3 install -r requirements.txt

# Change information in config file
.... more detail in the next step

# Run the tool
$ python3 main.py
```

## Setup config file

Open config.py

Fill your information including: publicKey, privateKey, and catIds of each wallet

Note: This tool helps cats in two wallets play with each other in order in the list (e.g. the first cat in catId of wallet1 will play date with the first cat in catId of wallet2, etc)

# Note

- If any error occur while running, please run it again.
- Use new wallets to ensure your safety.

# Thanks.
