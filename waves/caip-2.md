---
caip: 2
title: Waves Blockchain ID Specification
author: Maxim Smolyakov (@msmolyakov), Yury Sidorov (@darksyd94)
discussions-to: 
status: Draft
type: Standard
created: 2023-01-19
---

## Abstract

In CAIP-2 a general blockchain identification scheme is defined. This is the implementation of CAIP-2 for Waves network.

## Motivation

The final trigger to create this CAIP (and the CAIP process itself) was the need to publish the Waves blockchain and its ecosystem products in the [WalletConnect explorer](https://github.com/WalletConnect/walletconnect-monorepo/issues/1849).

## Specification

The blockchain ID (short "chain ID") is used while building account addresses, therefore, an address on one blockchain network cannot be used on another network. The chain ID is also indicated in transactions so it is impossible to move transactions between different blockchain networks.
