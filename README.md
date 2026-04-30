# Synthetic Trade Data Generator

A Python framework for generating synthetic financial trade data across multiple asset classes.  
Designed for testing pricing, risk, and analytics systems without requiring real market data.

---

## Overview

This project generates structured synthetic trades for:

- Rates (Bullet Bonds, IR Swaps)
- FX (Spot, Options)

Trade data can be exported in the following formats using their associated methods:

- Pandas DataFrame
- CSV
- List of dictionaries
- List of pydantic objects

---

## Quickstart Guide

This section demonstrates how to generate trades and export them to a CSV file.

### 1. Generate synthetic trades

```python
from trade_service import create_trades

# Generate 100 random trades across all asset classes as a `TradeCollection` object
trades = create_trades(n=100)
```
### 2. Call to_csv method from trades_collection object

```python
trades.to_csv("path/to/csv.csv")
```
---

## Features

- Synthetic trade generation across multiple asset classes
- Factory-based architecture per product type
- Common trade model with specialised extensions
- Randomised but structured financial attributes
- Optional sorting by trade date
- Export to DataFrame, CSV, or dictionaries

---

### Models

Pydantic models are used to represent each trade, with a base trade class extended for each specialised asset

Base trade model:

- Trade
  - trade_id
  - trade_date
  - asset_class
  - product_type
  - notional

Specialised models:

- BulletBond
- IRSwap
- FXOption
- FXSpot

---

### Factories

Each asset class has a dedicated factory responsible for generating synthetic trades:

- create_bullet_bond_trade()
- create_ir_swap_trade()
- create_fx_option_trade()
- create_fx_spot_trade()
