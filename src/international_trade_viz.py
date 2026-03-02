"""
International Trade Visualization
AGEC 370 - Agricultural Price Analysis

This module provides functions to plot domestic markets, foreign markets,
and resulting export supply/import demand curves for international trade analysis.

Author: AGEC 370 Course Materials
Date: November 2025
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Tuple, Optional

# Set style
sns.set_style("whitegrid")
plt.rcParams['font.family'] = 'Arial'

# UT Martin colors
UTM_BLUE = '#0b2341'
UTM_ORANGE = '#FF8200'


class TradeMarket:
    """
    Represents a domestic market with supply and demand functions.
    
    Parameters
    ----------
    supply_intercept : float
        Intercept of supply curve (Qs = supply_intercept + supply_slope * P)
    supply_slope : float
        Slope of supply curve
    demand_intercept : float
        Intercept of demand curve (Qd = demand_intercept - demand_slope * P)
    demand_slope : float
        Slope coefficient of demand curve (positive value)
    country_name : str
        Name of the country/market
    commodity : str
        Name of the commodity being traded
    """
    
    def __init__(self, supply_intercept: float, supply_slope: float,
                 demand_intercept: float, demand_slope: float,
                 country_name: str, commodity: str):
        self.supply_intercept = supply_intercept
        self.supply_slope = supply_slope
        self.demand_intercept = demand_intercept
        self.demand_slope = demand_slope
        self.country_name = country_name
        self.commodity = commodity
        
    def quantity_supplied(self, price: np.ndarray) -> np.ndarray:
        """Calculate quantity supplied at given price(s)."""
        return self.supply_intercept + self.supply_slope * price
    
    def quantity_demanded(self, price: np.ndarray) -> np.ndarray:
        """Calculate quantity demanded at given price(s)."""
        return self.demand_intercept - self.demand_slope * price
    
    def autarky_equilibrium(self) -> Tuple[float, float]:
        """
        Calculate autarky (no-trade) equilibrium price and quantity.
        
        Returns
        -------
        tuple
            (equilibrium_price, equilibrium_quantity)
        """
        # Qs = Qd: supply_intercept + supply_slope*P = demand_intercept - demand_slope*P
        p_eq = (self.demand_intercept - self.supply_intercept) / (self.supply_slope + self.demand_slope)
        q_eq = self.quantity_supplied(p_eq)
        return p_eq, q_eq

    # ES = Qs - Qd (Qs and Qd are functions of price)
    def export_supply(self, price: np.ndarray) -> np.ndarray:
        """Calculate export supply (Qs - Qd) at given price(s)."""
        return self.quantity_supplied(price) - self.quantity_demanded(price)
    
    # ID = Qd - Qs (Qd and Qs are functions of price)
    def import_demand(self, price: np.ndarray) -> np.ndarray:
        """Calculate import demand (Qd - Qs) at given price(s)."""
        return self.quantity_demanded(price) - self.quantity_supplied(price)


def find_world_equilibrium(exporter: TradeMarket, importer: TradeMarket) -> Tuple[float, float]:
    """
    Find world equilibrium price and quantity where ES = ID.
    
    Parameters
    ----------
    exporter : TradeMarket
        Market object for exporting country
    importer : TradeMarket
        Market object for importing country
        
    Returns
    -------
    tuple
        (world_price, trade_quantity)
    """
    # Export Supply: ES = (Qs - Qd) for exporter
    # Import Demand: ID = (Qd - Qs) for importer
    # ES = ID implies:
    # (supply_int_exp + slope_s_exp*P) - (demand_int_exp - slope_d_exp*P) = 
    # (demand_int_imp - slope_d_imp*P) - (supply_int_imp + slope_s_imp*P)
    
    # Simplifying: combine all terms with P on left, constants on right
    coef_p = (exporter.supply_slope + exporter.demand_slope + 
              importer.demand_slope + importer.supply_slope)
    constant = (importer.demand_intercept - importer.supply_intercept - 
                exporter.supply_intercept + exporter.demand_intercept)
    
    world_price = constant / coef_p
    trade_qty = exporter.export_supply(world_price) # or importer.import_demand(world_price); Plug in optimal world price to find optimal trade quantity
    
    return world_price, trade_qty


def find_world_equilibrium_with_tariff(exporter: TradeMarket, 
                                       importer: TradeMarket,
                                       tariff: float = 0) -> Tuple[float, float, float]:
    """
    Find equilibrium with tariff.
    
    Returns
    -------
    tuple
        (world_price, domestic_price_importer, trade_quantity)
    """
    if tariff == 0:
        p_world, q_trade = find_world_equilibrium(exporter, importer)
        return p_world, p_world, q_trade
    
    # With tariff: ES(P_world) = ID(P_world + tariff)
    # Iterative solution or algebraic (depends on complexity)
    # Export Supply: ES = (Qs - Qd) for exporter at P_world
    # Import Demand: ID = (Qd - Qs) for importer at (P_world + tariff)
    
    # Algebraically:
    # exporter.export_supply(P) = importer.import_demand(P + tariff)
    # ... solve for P_world ...
    
    # Simplified algebraic solution:
    coef_p = (exporter.supply_slope + exporter.demand_slope + 
              importer.demand_slope + importer.supply_slope)
    constant = (importer.demand_intercept - importer.supply_intercept - 
                exporter.supply_intercept + exporter.demand_intercept -
                tariff * (importer.demand_slope + importer.supply_slope))
    
    p_world = constant / coef_p
    p_domestic = p_world + tariff
    q_trade = exporter.export_supply(p_world) # Finds equilibrium trade quantity at world price
    
    return p_world, p_domestic, q_trade


def plot_trade_analysis(exporter: TradeMarket, importer: TradeMarket,
                        show_shifts: bool = False,
                        exporter_supply_shift: float = 0,
                        exporter_demand_shift: float = 0,
                        importer_supply_shift: float = 0,
                        importer_demand_shift: float = 0,
                        tariff: float = 0,
                        commodity_unit: str = "", 
                        commodity_per_unit: str = "",
                        figsize: Tuple[float, float] = (18, 5),
                        price_range: Optional[Tuple[float, float]] = None) -> plt.Figure:
    """
    Create three-panel visualization of international trade.
    
    Parameters
    ----------
    exporter : TradeMarket
        Market object for exporting country
    importer : TradeMarket
        Market object for importing country
    show_shifts : bool, default=False
        Whether to show shifted supply/demand curves
    exporter_supply_shift : float, default=0
        Shift in exporter's supply intercept
    exporter_demand_shift : float, default=0
        Shift in exporter's demand intercept
    importer_supply_shift : float, default=0
        Shift in importer's supply intercept
    importer_demand_shift : float, default=0
        Shift in importer's demand intercept
    tariff : float, default=0
        Specific tariff imposed on imports 
    commodity_unit : str, default=""
        Unit of commodity quantity (e.g., "million tons")
    commodity_per_unit : str, default=""
        Unit of commodity price (e.g., "ton")
    figsize : tuple, default=(18, 5)
        Figure size (width, height)
    price_range : tuple, optional
        (min_price, max_price) for plot range. If None, automatically determined.
        
    Returns
    -------
    matplotlib.figure.Figure
        The created figure object
    """
    
    # Determine price range if not provided
    if price_range is None:
        p_exp_autarky, _ = exporter.autarky_equilibrium()
        p_imp_autarky, _ = importer.autarky_equilibrium()
        p_world, _ = find_world_equilibrium(exporter, importer)
        
        p_min = min(p_exp_autarky, p_imp_autarky, p_world) * 0.8
        p_max = max(p_exp_autarky, p_imp_autarky, p_world) * 1.2
    else:
        p_min, p_max = price_range
    
    prices = np.linspace(p_min, p_max, 500)
    
    # Create figure with three subplots
    fig, axes = plt.subplots(1, 3, figsize=figsize)
    
    # ============ PANEL A: EXPORTER'S DOMESTIC MARKET ============
    ax1 = axes[0]
    
    # Original curves
    qs_exp = exporter.quantity_supplied(prices)
    qd_exp = exporter.quantity_demanded(prices)
    
    ax1.plot(qs_exp, prices, linewidth=2.5, color=UTM_BLUE, label='Supply', linestyle='-')
    ax1.plot(qd_exp, prices, linewidth=2.5, color=UTM_ORANGE, label='Demand', linestyle='-')
    
    # Autarky equilibrium
    p_aut_exp, q_aut_exp = exporter.autarky_equilibrium()
    ax1.plot(q_aut_exp, p_aut_exp, 'o', markersize=10, color='black', zorder=5)
    ax1.axhline(y=p_aut_exp, color='gray', linestyle='--', alpha=0.5, linewidth=1)
    ax1.axvline(x=q_aut_exp, color='gray', linestyle='--', alpha=0.5, linewidth=1)
    ax1.text(q_aut_exp * 1.30, p_aut_exp * 0.90, f'Autarky\nP=${p_aut_exp:.0f}\nQ={q_aut_exp:.0f}',
            fontsize=9, ha='right', va='bottom', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # World price line (with tariff if applicable)
    p_world, p_domestic_imp, _ = find_world_equilibrium_with_tariff(exporter, importer, tariff)
    ax1.axhline(y=p_world, color='darkgreen', linestyle=':', linewidth=2, alpha=0.7)
    
    # Show quantities at world price
    qs_world = exporter.quantity_supplied(p_world)
    qd_world = exporter.quantity_demanded(p_world)
    exports = qs_world - qd_world
    
    ax1.plot(qs_world, p_world, 's', markersize=8, color=UTM_BLUE, zorder=5)
    ax1.plot(qd_world, p_world, 's', markersize=8, color=UTM_ORANGE, zorder=5)
    ax1.text(qs_world * 1.02, p_world * 0.98, f'Qs={qs_world:.0f}', fontsize=8, va='top')
    ax1.text(qd_world * 0.98, p_world * 0.98, f'Qd={qd_world:.0f}', fontsize=8, va='top', ha='right')
    
    # Shade export region
    if exports > 0:
        ax1.fill_betweenx([p_world * 0.99, p_world * 1.01], qd_world, qs_world,
                          alpha=0.2, color='green', label=f'Exports={exports:.0f}')
    
    # Shifted curves if requested
    if show_shifts and (exporter_supply_shift != 0 or exporter_demand_shift != 0):
        exporter_shifted = TradeMarket(
            exporter.supply_intercept + exporter_supply_shift,
            exporter.supply_slope,
            exporter.demand_intercept + exporter_demand_shift,
            exporter.demand_slope,
            exporter.country_name,
            exporter.commodity
        )
        qs_shift = exporter_shifted.quantity_supplied(prices)
        qd_shift = exporter_shifted.quantity_demanded(prices)
        ax1.plot(qs_shift, prices, linewidth=2, color=UTM_BLUE, linestyle='--', alpha=0.6, label="Supply'")
        ax1.plot(qd_shift, prices, linewidth=2, color=UTM_ORANGE, linestyle='--', alpha=0.6, label="Demand'")
    
    ax1.set_xlabel(f'Quantity ({commodity_unit})', fontsize=11, fontweight='bold')
    ax1.set_ylabel(f'Price ($/{commodity_per_unit})', fontsize=11, fontweight='bold')
    ax1.set_title(f'Panel A: {exporter.country_name} Domestic Market\n({exporter.commodity})',
                  fontsize=12, fontweight='bold', color=UTM_BLUE)
    ax1.legend(loc='best', fontsize=9, framealpha=0.9)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(left=0)
    
    # ============ PANEL B: IMPORTER'S DOMESTIC MARKET ============
    ax2 = axes[1]
    
    # Original curves
    qs_imp = importer.quantity_supplied(prices)
    qd_imp = importer.quantity_demanded(prices)
    
    ax2.plot(qs_imp, prices, linewidth=2.5, color=UTM_BLUE, label='Supply', linestyle='-')
    ax2.plot(qd_imp, prices, linewidth=2.5, color=UTM_ORANGE, label='Demand', linestyle='-')
    
    # Autarky equilibrium
    p_aut_imp, q_aut_imp = importer.autarky_equilibrium()
    ax2.plot(q_aut_imp, p_aut_imp, 'o', markersize=10, color='black', zorder=5)
    ax2.axhline(y=p_aut_imp, color='gray', linestyle='--', alpha=0.5, linewidth=1)
    ax2.axvline(x=q_aut_imp, color='gray', linestyle='--', alpha=0.5, linewidth=1)
    ax2.text(q_aut_imp * 1.10, p_aut_imp * 0.90, f'Autarky\nP=${p_aut_imp:.0f}\nQ={q_aut_imp:.0f}',
             fontsize=9, ha='left', va='bottom', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    # Price lines: Show both world price and domestic price if tariff exists
    if tariff > 0:
        # Show world price (what exporters receive)
        ax2.axhline(y=p_world, color='darkgreen', linestyle=':', linewidth=2, alpha=0.5,
                   label=f'World Price = ${p_world:.0f}')
        # Show domestic price (what domestic consumers pay with tariff)
        ax2.axhline(y=p_domestic_imp, color='darkviolet', linestyle=':', linewidth=2.5, alpha=0.7,
                   label=f'Domestic Price = ${p_domestic_imp:.0f}')

        # Quantities are determined by domestic price (what consumers actually pay)
        qs_world_imp = importer.quantity_supplied(p_domestic_imp)
        qd_world_imp = importer.quantity_demanded(p_domestic_imp)
        imports = qd_world_imp - qs_world_imp

        # Plot quantities at domestic price
        ax2.plot(qs_world_imp, p_domestic_imp, 's', markersize=8, color=UTM_BLUE, zorder=5)
        ax2.plot(qd_world_imp, p_domestic_imp, 's', markersize=8, color=UTM_ORANGE, zorder=5)
        ax2.text(qs_world_imp * 0.92, p_domestic_imp * 0.98, f'Qs={qs_world_imp:.0f}',
                fontsize=8, va='top', ha='right')
        ax2.text(qd_world_imp * 1.02, p_domestic_imp * 0.98, f'Qd={qd_world_imp:.0f}',
                fontsize=8, va='top')

        # Shade tariff revenue (rectangle between world and domestic price)
        if imports > 0:
            ax2.fill_betweenx([p_world, p_domestic_imp], qs_world_imp, qd_world_imp,
                             alpha=0.15, color='darkviolet',
                             label=f'Tariff Revenue = ${tariff * imports:.0f}')
            # Also shade import region at domestic price
            ax2.fill_betweenx([p_domestic_imp * 0.995, p_domestic_imp * 1.005],
                             qs_world_imp, qd_world_imp,
                             alpha=0.2, color='purple', label=f'Imports = {imports:.0f}')
    else:
        # No tariff: standard visualization
        ax2.axhline(y=p_world, color='darkgreen', linestyle=':', linewidth=2, alpha=0.7)

        # Show quantities at world price
        qs_world_imp = importer.quantity_supplied(p_world)
        qd_world_imp = importer.quantity_demanded(p_world)
        imports = qd_world_imp - qs_world_imp

        ax2.plot(qs_world_imp, p_world, 's', markersize=8, color=UTM_BLUE, zorder=5)
        ax2.plot(qd_world_imp, p_world, 's', markersize=8, color=UTM_ORANGE, zorder=5)
        ax2.text(qs_world_imp * 0.92, p_world * 0.98, f'Qs={qs_world_imp:.0f}',
                fontsize=8, va='top', ha='right')
        ax2.text(qd_world_imp * 1.02, p_world * 0.98, f'Qd={qd_world_imp:.0f}',
                fontsize=8, va='top')

        # Shade import region
        if imports > 0:
            ax2.fill_betweenx([p_world * 0.99, p_world * 1.01], qs_world_imp, qd_world_imp,
                              alpha=0.2, color='purple', label=f'Imports={imports:.0f}')
    
    # Shifted curves if requested
    if show_shifts and (importer_supply_shift != 0 or importer_demand_shift != 0):
        importer_shifted = TradeMarket(
            importer.supply_intercept + importer_supply_shift,
            importer.supply_slope,
            importer.demand_intercept + importer_demand_shift,
            importer.demand_slope,
            importer.country_name,
            importer.commodity
        )
        qs_shift = importer_shifted.quantity_supplied(prices)
        qd_shift = importer_shifted.quantity_demanded(prices)
        ax2.plot(qs_shift, prices, linewidth=2, color=UTM_BLUE, linestyle='--', alpha=0.6, label="Supply'")
        ax2.plot(qd_shift, prices, linewidth=2, color=UTM_ORANGE, linestyle='--', alpha=0.6, label="Demand'")
    
    ax2.set_xlabel(f'Quantity ({commodity_unit})', fontsize=11, fontweight='bold')
    ax2.set_ylabel(f'Price ($/{commodity_per_unit})', fontsize=11, fontweight='bold')
    ax2.set_title(f'Panel B: {importer.country_name} Domestic Market\n({importer.commodity})',
                  fontsize=12, fontweight='bold', color=UTM_BLUE)
    ax2.legend(loc='best', fontsize=9, framealpha=0.9)
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(left=0)
    
    # ============ PANEL C: WORLD MARKET (ES and ID) ============
    ax3 = axes[2]
    
    # Calculate export supply and import demand
    es_qty = exporter.export_supply(prices)
    id_qty = importer.import_demand(prices)

    # Only plot positive values (countries export/import at relevant prices)
    es_positive = es_qty >= 0
    id_positive = id_qty >= 0

    # Plot Export Supply curve
    ax3.plot(es_qty[es_positive], prices[es_positive], linewidth=2.5,
             color=UTM_BLUE, label=f'{exporter.country_name} Export Supply', linestyle='-')

    # Handle tariff effects on Import Demand curve
    if tariff > 0:
        # Show original ID curve (without tariff) as reference
        ax3.plot(id_qty[id_positive], prices[id_positive], linewidth=2,
                 color=UTM_ORANGE, linestyle='--', alpha=0.4,
                 label=f'{importer.country_name} ID (no tariff)')

        # Calculate effective ID curve with tariff
        # At each world price P, importers face P+tariff domestically
        # So ID_effective(P_world) = ID_original(P_world + tariff)
        prices_with_tariff = prices + tariff  # Domestic prices importers face
        id_with_tariff = importer.import_demand(prices_with_tariff)
        id_tariff_positive = id_with_tariff >= 0

        # Plot shifted ID curve (with tariff) - this is what exporters see
        ax3.plot(id_with_tariff[id_tariff_positive], prices[id_tariff_positive],
                 linewidth=2.5, color='darkviolet', linestyle='-',
                 label=f'{importer.country_name} ID (with ${tariff:.0f} tariff)')

        # World equilibrium with tariff
        ax3.plot(exports, p_world, 'o', markersize=12, color='darkviolet', zorder=5,
                label=f'Equilibrium (with tariff)')
        ax3.axhline(y=p_world, color='darkviolet', linestyle='--', alpha=0.5, linewidth=1)
        ax3.axvline(x=exports, color='darkviolet', linestyle='--', alpha=0.5, linewidth=1)
        ax3.text(exports * 1.10, p_world * 1.10,
                 f'World Equilibrium\nP (World)=${p_world:.0f}\nP (Domestic)=${p_domestic_imp:.0f}\nQ={exports:.0f}',
                 fontsize=9, ha='left', va='bottom',
                 bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    else:
        # No tariff: standard visualization
        ax3.plot(id_qty[id_positive], prices[id_positive], linewidth=2.5,
                 color=UTM_ORANGE, label=f'{importer.country_name} Import Demand', linestyle='-')

        # World equilibrium
        ax3.plot(exports, p_world, 'o', markersize=12, color='darkgreen', zorder=5,
                label='World Equilibrium')
        ax3.axhline(y=p_world, color='darkgreen', linestyle='--', alpha=0.5, linewidth=1)
        ax3.axvline(x=exports, color='darkgreen', linestyle='--', alpha=0.5, linewidth=1)
        ax3.text(exports * 1.10, p_world * 1.10,
                 f'World Equilibrium\nP=${p_world:.0f}\nQ={exports:.0f}',
                 fontsize=9, ha='left', va='bottom',
                 bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # Shifted curves if requested
    if show_shifts and (exporter_supply_shift != 0 or exporter_demand_shift != 0 or
                       importer_supply_shift != 0 or importer_demand_shift != 0):
        exporter_shifted = TradeMarket(
            exporter.supply_intercept + exporter_supply_shift,
            exporter.supply_slope,
            exporter.demand_intercept + exporter_demand_shift,
            exporter.demand_slope,
            exporter.country_name,
            exporter.commodity
        )
        importer_shifted = TradeMarket(
            importer.supply_intercept + importer_supply_shift,
            importer.supply_slope,
            importer.demand_intercept + importer_demand_shift,
            importer.demand_slope,
            importer.country_name,
            importer.commodity
        )
        
        es_shift = exporter_shifted.export_supply(prices)
        id_shift = importer_shifted.import_demand(prices)
        
        es_pos_shift = es_shift >= 0
        id_pos_shift = id_shift >= 0
        
        ax3.plot(es_shift[es_pos_shift], prices[es_pos_shift], linewidth=2, 
                 color=UTM_BLUE, linestyle='--', alpha=0.6, label="Export Supply'")
        ax3.plot(id_shift[id_pos_shift], prices[id_pos_shift], linewidth=2, 
                 color=UTM_ORANGE, linestyle='--', alpha=0.6, label="Import Demand'")
        
        # New equilibrium
        p_world_new, trade_new = find_world_equilibrium(exporter_shifted, importer_shifted)
        ax3.plot(trade_new, p_world_new, 's', markersize=10, color='darkgreen', 
                 zorder=5, alpha=0.7, label="New Equilibrium")
        ax3.text(trade_new * 0.95, p_world_new * 0.98, 
                 f"New: P=${p_world_new:.0f}, Q={trade_new:.0f}",
                 fontsize=8, ha='right', va='top',
                 bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    
    ax3.set_xlabel(f'Trade Quantity ({commodity_unit})', fontsize=11, fontweight='bold')
    ax3.set_ylabel(f'Price ($/{commodity_per_unit})', fontsize=11, fontweight='bold')
    ax3.set_title(f'Panel C: World Market\n(Export Supply & Import Demand)',
                  fontsize=12, fontweight='bold', color=UTM_BLUE)
    ax3.legend(loc='best', fontsize=9, framealpha=0.9)
    ax3.grid(True, alpha=0.3)
    ax3.set_xlim(left=0)
    
    plt.tight_layout()
    
    return fig


# ============ EXAMPLE: US-COSTA RICA RICE TRADE ============

if __name__ == "__main__":
    
    # Define US market (exporter)
    us_market = TradeMarket(
        supply_intercept=-200,
        supply_slope=1.0,
        demand_intercept=800,
        demand_slope=0.5,
        country_name="United States",
        commodity="Rice"
    )
    
    # Define Costa Rica market (importer)
    costa_rica_market = TradeMarket(
        supply_intercept=-100,
        supply_slope=0.5,
        demand_intercept=600,
        demand_slope=0.25,
        country_name="Costa Rica",
        commodity="Rice"
    )
    
    # Create output directory if it doesn't exist
    from pathlib import Path
    output_dir = Path(__file__).parent.parent / 'output' / 'figures'
    output_dir.mkdir(parents=True, exist_ok=True)

    # Create baseline visualization
    print("Creating baseline trade visualization...")
    fig1 = plot_trade_analysis(us_market, costa_rica_market,
                               price_range=(500, 1000))
    plt.savefig(output_dir / 'trade_analysis_baseline.png', dpi=300, bbox_inches='tight')
    print(f"✓ Baseline saved as '{output_dir / 'trade_analysis_baseline.png'}'")

    # Example: Show effect of US supply increase (e.g., technological improvement)
    print("\nCreating visualization with US supply shift...")
    fig2 = plot_trade_analysis(us_market, costa_rica_market,
                               show_shifts=True,
                               exporter_supply_shift=100,  # US supply increases
                               price_range=(500, 1000))
    plt.savefig(output_dir / 'trade_analysis_supply_shift.png', dpi=300, bbox_inches='tight')
    print(f"✓ Supply shift saved as '{output_dir / 'trade_analysis_supply_shift.png'}'")

    # Example: Show effect of Costa Rica demand increase (e.g., population growth)
    print("\nCreating visualization with Costa Rica demand shift...")
    fig3 = plot_trade_analysis(us_market, costa_rica_market,
                               show_shifts=True,
                               importer_demand_shift=100,  # Costa Rica demand increases
                               price_range=(500, 1000))
    plt.savefig(output_dir / 'trade_analysis_demand_shift.png', dpi=300, bbox_inches='tight')
    print(f"✓ Demand shift saved as '{output_dir / 'trade_analysis_demand_shift.png'}'")

    # Example: Show effect of tariff imposed by Costa Rica
    print("\nCreating visualization with $50 tariff by Costa Rica...")
    fig4 = plot_trade_analysis(us_market, costa_rica_market,
                               tariff=50,  # $50/ton tariff
                               price_range=(500, 1000))
    plt.savefig(output_dir / 'trade_analysis_tariff.png', dpi=300, bbox_inches='tight')
    print(f"✓ Tariff analysis saved as '{output_dir / 'trade_analysis_tariff.png'}'")

    # plt.show()  # Comment out to avoid blocking in automated testing
    plt.close('all')  # Close all figures to free memory
    
    print("\n" + "="*60)
    print("EXAMPLE COMPLETE")
    print("="*60)
    print("\nMarket Summary:")
    print(f"US Autarky Price: ${us_market.autarky_equilibrium()[0]:.2f}/ton")
    print(f"Costa Rica Autarky Price: ${costa_rica_market.autarky_equilibrium()[0]:.2f}/ton")
    
    p_world, q_trade = find_world_equilibrium(us_market, costa_rica_market)
    print(f"\nWorld Equilibrium (no tariff):")
    print(f"  World Price: ${p_world:.2f}/ton")
    print(f"  Trade Volume: {q_trade:.2f} million tons")

    # Show tariff effects
    p_world_tariff, p_domestic_tariff, q_trade_tariff = find_world_equilibrium_with_tariff(
        us_market, costa_rica_market, tariff=50)
    print(f"\nWith $50 Tariff:")
    print(f"  World Price: ${p_world_tariff:.2f}/ton")
    print(f"  Costa Rica Domestic Price: ${p_domestic_tariff:.2f}/ton")
    print(f"  Trade Volume: {q_trade_tariff:.2f} million tons")
    print(f"  Trade Reduction: {q_trade - q_trade_tariff:.2f} million tons ({((q_trade - q_trade_tariff)/q_trade * 100):.1f}%)")
    print(f"  Tariff Revenue: ${50 * q_trade_tariff:.2f}")
