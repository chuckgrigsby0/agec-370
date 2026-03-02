"""
Supply and Demand Visualization Basics
AGEC 370 - Agricultural Price Analysis

This module provides simple, flexible functions for creating educational
supply and demand visualizations for teaching microeconomic principles.

Author: AGEC 370 Course Materials
Date: January 2026
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Tuple, Optional, List

# Set visualization style
sns.set_style("whitegrid")
plt.rcParams['font.family'] = 'Arial'

# UT Martin institution colors
UTM_BLUE = '#0b2341'
UTM_ORANGE = '#FF8200'


class SupplyDemand:
    """
    Represents a single market with supply and demand functions.

    Supply: Qs = supply_intercept + supply_slope * P
    Demand: Qd = demand_intercept - demand_slope * P

    Parameters
    ----------
    supply_intercept : float
        Y-intercept of supply curve (Qs when P=0)
    supply_slope : float
        Slope of supply curve (change in Qs per unit change in P)
    demand_intercept : float
        Y-intercept of demand curve (Qd when P=0)
    demand_slope : float
        Slope coefficient of demand curve (positive value, represents sensitivity)
    commodity : str, default="Good"
        Name of the commodity
    price_unit : str, default="$"
        Unit for price (e.g., "$/bushel", "$")
    quantity_unit : str, default="units"
        Unit for quantity (e.g., "million bushels", "tons")
    """

    def __init__(self,
                 supply_intercept: float,
                 supply_slope: float,
                 demand_intercept: float,
                 demand_slope: float,
                 commodity: str = "Good",
                 price_unit: str = "$",
                 quantity_unit: str = "units"):
        self.supply_intercept = supply_intercept
        self.supply_slope = supply_slope
        self.demand_intercept = demand_intercept
        self.demand_slope = demand_slope
        self.commodity = commodity
        self.price_unit = price_unit
        self.quantity_unit = quantity_unit

    def quantity_supplied(self, price: np.ndarray) -> np.ndarray:
        """Calculate quantity supplied at given price(s)."""
        return self.supply_intercept + self.supply_slope * price

    def quantity_demanded(self, price: np.ndarray) -> np.ndarray:
        """Calculate quantity demanded at given price(s)."""
        return self.demand_intercept - self.demand_slope * price

    def equilibrium(self) -> Tuple[float, float]:
        """
        Calculate market equilibrium price and quantity.

        Returns
        -------
        tuple
            (equilibrium_price, equilibrium_quantity)
        """
        # Set Qs = Qd and solve for P
        # supply_intercept + supply_slope*P = demand_intercept - demand_slope*P
        p_eq = (self.demand_intercept - self.supply_intercept) / (self.supply_slope + self.demand_slope)
        q_eq = self.quantity_supplied(p_eq)
        return p_eq, q_eq


def plot_supply_demand(market: SupplyDemand,
                       figsize: Tuple[float, float] = (10, 7),
                       price_range: Optional[Tuple[float, float]] = None,
                       show_equilibrium: bool = True,
                       show_supply: bool = True,
                       show_demand: bool = True,
                       supply_name: str = 'Supply',
                       demand_name: str = 'Demand',
                       supply_vertical_lines: Optional[List[float]] = None,
                       demand_vertical_lines: Optional[List[float]] = None,
                       title: Optional[str] = None,
                       ax: Optional[plt.Axes] = None) -> plt.Figure:
    """
    Create a basic supply and demand plot.

    Parameters
    ----------
    market : SupplyDemand
        Market object containing supply/demand parameters
    figsize : tuple, default=(10, 7)
        Figure size (width, height) in inches
    price_range : tuple, optional
        (min_price, max_price) for y-axis. If None, auto-determined.
    show_equilibrium : bool, default=True
        Whether to mark the equilibrium point
    show_supply : bool, default=True
        Whether to plot the supply curve
    show_demand : bool, default=True
        Whether to plot the demand curve
    supply_name: str, default='Supply'
        Custom label for supply curve in legend
    demand_name: str, default='Demand'
        Custom label for demand curve in legend
    supply_vertical_lines : list of float, optional
        List of quantity values where vertical dashed lines should be drawn,
        stopping at the supply curve
    demand_vertical_lines : list of float, optional
        List of quantity values where vertical dashed lines should be drawn,
        stopping at the demand curve
    title : str, optional
        Custom title for the plot. If None, uses default.
    ax : matplotlib.axes.Axes, optional
        Existing axes to plot on. If None, creates new figure.

    Returns
    -------
    matplotlib.figure.Figure
        The created or modified figure
    """
    # Create figure if not provided
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.get_figure()

    # Determine price range
    if price_range is None:
        p_eq, q_eq = market.equilibrium()
        # Set range from 0 to 1.5x equilibrium price
        p_min = 0
        p_max = p_eq * 1.5
    else:
        p_min, p_max = price_range

    # Generate price array for plotting
    prices = np.linspace(p_min, p_max, 500)

    # Calculate quantities
    qs = market.quantity_supplied(prices)
    qd = market.quantity_demanded(prices)

    # Plot supply curve (blue, upward sloping)
    if show_supply:
        ax.plot(qs, prices,
                linewidth=3.0,
                color=UTM_BLUE,
                label=supply_name,
                zorder=2)

    # Plot demand curve (orange, downward sloping)
    if show_demand:
        ax.plot(qd, prices,
                linewidth=3.0,
                color=UTM_ORANGE,
                label=demand_name,
                zorder=2)

    # Draw vertical dashed lines at specified quantities (stopping at supply curve)
    if supply_vertical_lines:
        for q in supply_vertical_lines:
            # Calculate price on supply curve at this quantity
            p_at_q = (q - market.supply_intercept) / market.supply_slope
            # Draw line from x-axis up to supply curve
            ax.vlines(x=q, ymin=0, ymax=p_at_q,
                        color='black', linestyle='--', alpha=0.6, linewidth=2, zorder=1)

    # Draw vertical dashed lines at specified quantities (stopping at demand curve)
    if demand_vertical_lines:
        for q in demand_vertical_lines:
            # Calculate price on demand curve at this quantity
            p_at_q = (market.demand_intercept - q) / market.demand_slope
            # Draw line from x-axis up to demand curve
            ax.vlines(x=q, ymin=0, ymax=p_at_q,
                        color='black', linestyle='--', alpha=0.6, linewidth=2, zorder=1)


    # Mark equilibrium if requested
    if show_equilibrium:
        p_eq, q_eq = market.equilibrium()

        # Plot equilibrium point (black dot on top of curves)
        ax.plot(q_eq, p_eq, 'o', markersize=10, color='black', zorder=5)

        # Add horizontal price line (using data coordinates)
        ax.hlines(y=p_eq, xmin=0, xmax=q_eq, color='black', linestyle=':', linewidth=3, alpha=0.7, zorder=3)
        ax.vlines(x=q_eq, ymin=0, ymax=p_eq, color='black', linestyle=':', alpha=0.7, linewidth=2, zorder=1)

        # Annotate equilibrium point with rounded text box
        # ax.text(q_eq * 1.1, p_eq * 1.05,
        #         f'Equilibrium\nP = {p_eq:.1f}\nQ = {q_eq:.1f}',
        #         fontsize=9, ha='left', va='bottom',
        #         bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        ax.text(q_eq * 0.05, p_eq * 1.02, f'Price = {p_eq:.1f}',
           fontsize=14, va='bottom', color='black', fontweight='bold')
        
        ax.text(q_eq * 1.02, p_eq * 0.05, f'Quantity = {q_eq:.1f}',
           fontsize=14, va='bottom', color='black', fontweight='bold')

    # Configure axes labels
    ax.set_xlabel(f'Quantity ({market.quantity_unit})', fontsize=16, fontweight='bold')
    ax.set_ylabel(f'Price ({market.price_unit})', fontsize=16, fontweight='bold')

    # Set title
    if title is None:
        title = f'Supply and Demand: {market.commodity}'
    ax.set_title(title, fontsize=20, fontweight='bold')

    # Add legend (upper right corner, semi-transparent background)
    ax.legend(loc='best', fontsize=12, framealpha=0.9)

    # Enable grid (subtle, alpha=0.5 for light appearance)
    ax.grid(True, alpha=0.5)

    # Set x-axis to start at 0 (no negative quantities)
    ax.set_xlim(left=0)

    plt.tight_layout()

    return fig


def plot_shift_comparison(original_market: SupplyDemand,
                          shifted_market: SupplyDemand,
                          shift_type: str,
                          figsize: Tuple[float, float] = (16, 7),
                          price_range: Optional[Tuple[float, float]] = None,
                          show_other_curve: bool = True,
                          show_equilibrium: bool = True,
                          single_panel: bool = False) -> plt.Figure:
    """
    Create comparison showing supply or demand shift effects.

    Parameters
    ----------
    original_market : SupplyDemand
        Market before the shift
    shifted_market : SupplyDemand
        Market after the shift
    shift_type : str
        Type of shift: 'supply' or 'demand'
    figsize : tuple, default=(16, 7)
        Figure size (width, height) in inches. For single_panel=True,
        width is automatically halved.
    price_range : tuple, optional
        (min_price, max_price) for consistent y-axis across panels.
        If None, auto-determined from equilibria.
    show_other_curve : bool, default=True
        Whether to show the non-shifting curve (demand for supply shifts,
        supply for demand shifts)
    show_equilibrium : bool, default=True
        Whether to mark old and new equilibrium points
    single_panel : bool, default=False
        If True, creates a single panel showing the shift instead of
        side-by-side comparison

    Returns
    -------
    matplotlib.figure.Figure
        The created figure (one or two panels based on single_panel)
    """
    # Create figure - single panel or two side-by-side panels
    if single_panel:
        fig, ax_main = plt.subplots(figsize=(figsize[0] / 2, figsize[1]))
    else:
        fig, (ax_main, ax_right) = plt.subplots(1, 2, figsize=figsize)

    # Determine price range if not specified
    if price_range is None:
        p_eq_old, _ = original_market.equilibrium()
        p_eq_new, _ = shifted_market.equilibrium()
        p_min = 0
        p_max = max(p_eq_old, p_eq_new) * 1.5
    else:
        p_min, p_max = price_range

    prices = np.linspace(p_min, p_max, 500)

    # Determine shift direction
    if shift_type.lower() == 'supply':
        # Supply shift: compare supply intercepts
        shift_direction = 'increase' if shifted_market.supply_intercept > original_market.supply_intercept else 'decrease'
    else:  # demand shift
        # Demand shift: compare demand intercepts
        shift_direction = 'increase' if shifted_market.demand_intercept > original_market.demand_intercept else 'decrease'

    # Get equilibria
    p_eq_old, q_eq_old = original_market.equilibrium()
    p_eq_new, q_eq_new = shifted_market.equilibrium()

    # ============ MAIN PANEL: Shift visualization ============
    if shift_type.lower() == 'supply':
        # Plot original supply and demand
        qs_old = original_market.quantity_supplied(prices)
        qd = original_market.quantity_demanded(prices)  # Demand doesn't change

        # Plot demand curve (stays the same) - only if show_other_curve is True
        if show_other_curve:
            ax_main.plot(qd, prices, linewidth=3.0, color=UTM_ORANGE, label='Demand', zorder=2)

        # Plot original supply (solid)
        ax_main.plot(qs_old, prices, linewidth=3.0, color=UTM_BLUE,
                    label='Original Supply', zorder=2)
        
        # Plot new supply (dashed to show it's the shifted curve)
        qs_new = shifted_market.quantity_supplied(prices)
        ax_main.plot(qs_new, prices, linewidth=3.0, color=UTM_BLUE,
                    linestyle='--', label='New Supply', zorder=1)
        
        if show_other_curve:
            # Add old and new equilibrium price and quantity dashed lines. 
            ax_main.hlines(y=p_eq_old, xmin=0, xmax=q_eq_old,
                        color='gray', linestyle=':', linewidth=2, alpha=0.7, zorder=3)
            ax_main.hlines(y=p_eq_new, xmin=0, xmax=q_eq_new,
                        color='gray', linestyle='--', linewidth=2, alpha=0.7, zorder=3)
            # Vertical line at old quantity (gray)
            ax_main.vlines(x=q_eq_old, ymin=0, ymax=p_eq_old,
                        color='black', linestyle=':', alpha=0.7, linewidth=2, zorder=1)
            # Vertical line at new quantity at old price (black)
            ax_main.vlines(x=q_eq_new, ymin=0, ymax=p_eq_new,
                        color='black', linestyle='--', alpha=0.7, linewidth=2, zorder=1)
        else:
            # Calculate quantity on NEW supply curve at OLD price (for dashed lines)
            q_new_at_old_price = shifted_market.quantity_supplied(p_eq_old)

            # Add dashed lines showing quantity change at constant price (textbook style)
            # Horizontal line at old price, extending to the further quantity
            ax_main.hlines(y=p_eq_old, xmin=0, xmax=max(q_eq_old, q_new_at_old_price),
                        color='gray', linestyle=':', linewidth=2, alpha=0.7, zorder=3)
            # Vertical line at old quantity (gray)
            ax_main.vlines(x=q_eq_old, ymin=0, ymax=p_eq_old,
                        color='gray', linestyle='--', alpha=0.7, linewidth=2, zorder=1)
            # Vertical line at new quantity at old price (black)
            ax_main.vlines(x=q_new_at_old_price, ymin=0, ymax=p_eq_old,
                        color='black', linestyle='--', alpha=0.7, linewidth=2, zorder=1)

        # Add arrow annotation showing shift direction
        arrow_p = p_eq_old * 1.1
        arrow_q_start = original_market.quantity_supplied(arrow_p)
        arrow_q_end = shifted_market.quantity_supplied(arrow_p)

        if shift_direction == 'increase':
            ax_main.annotate('', xy=(arrow_q_end, arrow_p), xytext=(arrow_q_start, arrow_p),
                           arrowprops=dict(arrowstyle='->', lw=3, color=UTM_ORANGE))
            panel_title = 'Supply Increase (Shifts Right)'
        else:
            ax_main.annotate('', xy=(arrow_q_end, arrow_p), xytext=(arrow_q_start, arrow_p),
                           arrowprops=dict(arrowstyle='->', lw=3, color=UTM_ORANGE))
            panel_title = 'Supply Decrease (Shifts Left)'

    else:  # demand shift
        # Plot original supply and demand
        qs = original_market.quantity_supplied(prices)  # Supply doesn't change
        qd_old = original_market.quantity_demanded(prices)

        # Plot supply curve (stays the same) - only if show_other_curve is True
        if show_other_curve:
            ax_main.plot(qs, prices, linewidth=3.0, color=UTM_BLUE, label='Supply', zorder=2)

        # Plot original demand (solid)
        ax_main.plot(qd_old, prices, linewidth=3.0, color=UTM_ORANGE,
                    label='Original Demand', zorder=2)

        # Plot new demand (dashed to show it's the shifted curve)
        qd_new = shifted_market.quantity_demanded(prices)
        ax_main.plot(qd_new, prices, linewidth=3.0, color=UTM_ORANGE,
                    linestyle='--', label='New Demand', zorder=1)
        

        if show_other_curve:
            # Add old and new equilibrium price and quantity dashed lines. 
            ax_main.hlines(y=p_eq_old, xmin=0, xmax=q_eq_old,
                        color='gray', linestyle=':', linewidth=2, alpha=0.7, zorder=3)
            ax_main.hlines(y=p_eq_new, xmin=0, xmax=q_eq_new,
                        color='gray', linestyle='--', linewidth=2, alpha=0.7, zorder=3)
            # Vertical line at old quantity (gray)
            ax_main.vlines(x=q_eq_old, ymin=0, ymax=p_eq_old,
                        color='black', linestyle=':', alpha=0.7, linewidth=2, zorder=1)
            # Vertical line at new quantity at old price (black)
            ax_main.vlines(x=q_eq_new, ymin=0, ymax=p_eq_new,
                        color='black', linestyle='--', alpha=0.7, linewidth=2, zorder=1)
        else:
            # Calculate quantity on NEW demand curve at OLD price (for dashed lines)
            q_new_at_old_price = shifted_market.quantity_demanded(p_eq_old)

            # Add dashed lines showing quantity change at constant price (textbook style)
            # Horizontal line at old price, extending to the further quantity
            ax_main.hlines(y=p_eq_old, xmin=0, xmax=max(q_eq_old, q_new_at_old_price),
                        color='gray', linestyle=':', linewidth=2, alpha=0.7, zorder=3)
            # Vertical line at old quantity (gray)
            ax_main.vlines(x=q_eq_old, ymin=0, ymax=p_eq_old,
                        color='gray', linestyle='--', alpha=0.7, linewidth=2, zorder=1)
            # Vertical line at new quantity at old price (black)
            ax_main.vlines(x=q_new_at_old_price, ymin=0, ymax=p_eq_old,
                        color='black', linestyle='--', alpha=0.7, linewidth=2, zorder=1)

        # Add arrow annotation showing shift direction
        arrow_p = p_eq_old * 1.1
        arrow_q_start = original_market.quantity_demanded(arrow_p)
        arrow_q_end = shifted_market.quantity_demanded(arrow_p)

        if shift_direction == 'increase':
            ax_main.annotate('', xy=(arrow_q_end, arrow_p), xytext=(arrow_q_start, arrow_p),
                           arrowprops=dict(arrowstyle='->', mutation_scale=20, lw=3, color=UTM_ORANGE))
            panel_title = 'Demand Increase (Shifts Right)'
        else:
            ax_main.annotate('', xy=(arrow_q_end, arrow_p), xytext=(arrow_q_start, arrow_p),
                           arrowprops=dict(arrowstyle='->', mutation_scale=20, lw=3, color=UTM_ORANGE))
            panel_title = 'Demand Decrease (Shifts Left)'

    # Mark old and new equilibria on main panel
    if show_equilibrium:
        ax_main.plot(q_eq_old, p_eq_old, 'o', markersize=10, color='gray',
                    zorder=4, label='Old Equilibrium')
        ax_main.plot(q_eq_new, p_eq_new, 'o', markersize=10, color='black',
                    zorder=5, label='New Equilibrium')

    # Configure main panel
    ax_main.set_xlabel(f'Quantity ({original_market.quantity_unit})', fontsize=16, fontweight='bold')
    ax_main.set_ylabel(f'Price ({original_market.price_unit})', fontsize=16, fontweight='bold')
    ax_main.set_title(panel_title, fontsize=20, fontweight='bold')
    ax_main.legend(loc='best', fontsize=12, framealpha=0.9)
    ax_main.grid(True, alpha=0.3)
    ax_main.set_xlim(left=0)
    ax_main.set_ylim([p_min, p_max])

    # ============ RIGHT PANEL: Equilibrium comparison (only if not single_panel) ============
    if not single_panel:
        if shift_type.lower() == 'supply':
            # Plot demand - only if show_other_curve is True
            if show_other_curve:
                ax_right.plot(qd, prices, linewidth=3.0, color=UTM_ORANGE, label='Demand', zorder=2)

            # Plot both supply curves (original solid, new dashed)
            ax_right.plot(qs_old, prices, linewidth=3.0, color=UTM_BLUE,
                         label='S (original)', zorder=2)
            ax_right.plot(qs_new, prices, linewidth=3.0, color=UTM_BLUE,
                         linestyle='--', alpha=0.7, label='S (new)', zorder=1)
        else:
            # Plot supply - only if show_other_curve is True
            if show_other_curve:
                ax_right.plot(qs, prices, linewidth=3.0, color=UTM_BLUE, label='Supply', zorder=2)

            # Plot both demand curves (original solid, new dashed)
            ax_right.plot(qd_old, prices, linewidth=3.0, color=UTM_ORANGE,
                         label='D (original)', zorder=2)
            ax_right.plot(qd_new, prices, linewidth=3.0, color=UTM_ORANGE,
                         linestyle='--', alpha=0.7, label='D (new)', zorder=1)

        # Mark equilibria with labels on right panel
        if show_equilibrium:
            ax_right.plot(q_eq_old, p_eq_old, 'o', markersize=10, color='gray', zorder=4)
            ax_right.plot(q_eq_new, p_eq_new, 'o', markersize=10, color='black', zorder=5)

            # Add text annotations for equilibria
            ax_right.text(q_eq_old * 0.95, p_eq_old * 0.95, 'Old',
                        fontsize=14, ha='right', va='top',
                        bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.7))
            ax_right.text(q_eq_new * 1.05, p_eq_new * 1.05, 'New',
                        fontsize=14, ha='left', va='bottom',
                        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

        # Configure right panel
        ax_right.set_xlabel(f'Quantity ({original_market.quantity_unit})', fontsize=16, fontweight='bold')
        ax_right.set_ylabel(f'Price ({original_market.price_unit})', fontsize=16, fontweight='bold')
        ax_right.set_title('Equilibrium Comparison', fontsize=16, fontweight='bold')
        ax_right.legend(loc='best', fontsize=12, framealpha=0.9)
        ax_right.grid(True, alpha=0.3)
        ax_right.set_xlim(left=0)
        ax_right.set_ylim([p_min, p_max])

    plt.tight_layout()

    return fig


def plot_double_shift(original_market: SupplyDemand,
                      shifted_market: SupplyDemand,
                      figsize: Tuple[float, float] = (16, 7),
                      price_range: Optional[Tuple[float, float]] = None,
                      show_equilibrium: bool = True,
                      single_panel: bool = False) -> plt.Figure:
    """
    Create a plot showing simultaneous supply and demand shifts.

    Parameters
    ----------
    original_market : SupplyDemand
        Market before shifts
    shifted_market : SupplyDemand
        Market after both supply and demand have shifted
    figsize : tuple, default=(16, 7)
        Figure size (width, height) in inches. For single_panel=True,
        width is automatically halved.
    price_range : tuple, optional
        (min_price, max_price) for consistent y-axis across panels.
        If None, auto-determined from equilibria.
    show_equilibrium : bool, default=True
        Whether to mark old and new equilibrium points
    single_panel : bool, default=False
        If True, creates a single panel instead of side-by-side comparison

    Returns
    -------
    matplotlib.figure.Figure
        The created figure
    """
    # Create figure layout
    if single_panel:
        fig, ax_main = plt.subplots(figsize=(figsize[0] / 2, figsize[1]))
    else:
        fig, (ax_main, ax_right) = plt.subplots(1, 2, figsize=figsize)

    # Determine price range if not specified
    if price_range is None:
        p_eq_old, _ = original_market.equilibrium()
        p_eq_new, _ = shifted_market.equilibrium()
        p_min = 0
        p_max = max(p_eq_old, p_eq_new) * 1.5
    else:
        p_min, p_max = price_range

    prices = np.linspace(p_min, p_max, 500)

    # Determine shift directions for labeling
    supply_direction = 'increase' if shifted_market.supply_intercept > original_market.supply_intercept else 'decrease'
    demand_direction = 'increase' if shifted_market.demand_intercept > original_market.demand_intercept else 'decrease'

    # Get equilibria
    p_eq_old, q_eq_old = original_market.equilibrium()
    p_eq_new, q_eq_new = shifted_market.equilibrium()

    # Calculate all four curves
    qs_old = original_market.quantity_supplied(prices)
    qs_new = shifted_market.quantity_supplied(prices)
    qd_old = original_market.quantity_demanded(prices)
    qd_new = shifted_market.quantity_demanded(prices)

    # ============ MAIN PANEL ============
    # Original curves (solid)
    ax_main.plot(qs_old, prices, linewidth=3.0, color=UTM_BLUE,
                 label='Original Supply', zorder=2)
    ax_main.plot(qd_old, prices, linewidth=3.0, color=UTM_ORANGE,
                 label='Original Demand', zorder=2)

    # Shifted curves (dashed)
    ax_main.plot(qs_new, prices, linewidth=3.0, color=UTM_BLUE,
                 linestyle='--', label='New Supply', zorder=1)
    ax_main.plot(qd_new, prices, linewidth=3.0, color=UTM_ORANGE,
                 linestyle='--', label='New Demand', zorder=1)

    # Equilibrium reference lines
    ax_main.hlines(y=p_eq_old, xmin=0, xmax=q_eq_old,
                   color='gray', linestyle=':', linewidth=2, alpha=0.7, zorder=3)
    ax_main.hlines(y=p_eq_new, xmin=0, xmax=q_eq_new,
                   color='gray', linestyle='--', linewidth=2, alpha=0.7, zorder=3)
    ax_main.vlines(x=q_eq_old, ymin=0, ymax=p_eq_old,
                   color='black', linestyle=':', alpha=0.7, linewidth=2, zorder=1)
    ax_main.vlines(x=q_eq_new, ymin=0, ymax=p_eq_new,
                   color='black', linestyle='--', alpha=0.7, linewidth=2, zorder=1)

    # Supply shift arrow
    arrow_p_s = p_eq_old * 1.15
    arrow_qs_start = original_market.quantity_supplied(arrow_p_s)
    arrow_qs_end = shifted_market.quantity_supplied(arrow_p_s)
    ax_main.annotate('', xy=(arrow_qs_end, arrow_p_s), xytext=(arrow_qs_start, arrow_p_s),
                     arrowprops=dict(arrowstyle='->', lw=3, color=UTM_BLUE, alpha=0.6))

    # Demand shift arrow
    arrow_p_d = p_eq_old * 0.85
    arrow_qd_start = original_market.quantity_demanded(arrow_p_d)
    arrow_qd_end = shifted_market.quantity_demanded(arrow_p_d)
    ax_main.annotate('', xy=(arrow_qd_end, arrow_p_d), xytext=(arrow_qd_start, arrow_p_d),
                     arrowprops=dict(arrowstyle='->', lw=3, color=UTM_ORANGE, alpha=0.6))

    # Mark old and new equilibria
    if show_equilibrium:
        ax_main.plot(q_eq_old, p_eq_old, 'o', markersize=10, color='gray',
                     zorder=4, label='Old Equilibrium')
        ax_main.plot(q_eq_new, p_eq_new, 'o', markersize=10, color='black',
                     zorder=5, label='New Equilibrium')

    # Build descriptive title
    s_label = 'Increase' if supply_direction == 'increase' else 'Decrease'
    d_label = 'Increase' if demand_direction == 'increase' else 'Decrease'
    panel_title = f'Supply {s_label} + Demand {d_label}'

    # Configure main panel
    ax_main.set_xlabel(f'Quantity ({original_market.quantity_unit})', fontsize=16, fontweight='bold')
    ax_main.set_ylabel(f'Price ({original_market.price_unit})', fontsize=16, fontweight='bold')
    ax_main.set_title(panel_title, fontsize=20, fontweight='bold')
    ax_main.legend(loc='best', fontsize=12, framealpha=0.9)
    ax_main.grid(True, alpha=0.3)
    ax_main.set_xlim(left=0)
    ax_main.set_ylim([p_min, p_max])

    # ============ RIGHT PANEL: Equilibrium comparison ============
    if not single_panel:
        # Plot all four curves
        ax_right.plot(qs_old, prices, linewidth=3.0, color=UTM_BLUE,
                      label='S (original)', zorder=2)
        ax_right.plot(qs_new, prices, linewidth=3.0, color=UTM_BLUE,
                      linestyle='--', alpha=0.7, label='S (new)', zorder=1)
        ax_right.plot(qd_old, prices, linewidth=3.0, color=UTM_ORANGE,
                      label='D (original)', zorder=2)
        ax_right.plot(qd_new, prices, linewidth=3.0, color=UTM_ORANGE,
                      linestyle='--', alpha=0.7, label='D (new)', zorder=1)

        # Mark equilibria with labels
        if show_equilibrium:
            ax_right.plot(q_eq_old, p_eq_old, 'o', markersize=10, color='gray', zorder=4)
            ax_right.plot(q_eq_new, p_eq_new, 'o', markersize=10, color='black', zorder=5)

            ax_right.text(q_eq_old * 0.95, p_eq_old * 0.95, 'Old',
                          fontsize=14, ha='right', va='top',
                          bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.7))
            ax_right.text(q_eq_new * 1.05, p_eq_new * 1.05, 'New',
                          fontsize=14, ha='left', va='bottom',
                          bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

        # Configure right panel
        ax_right.set_xlabel(f'Quantity ({original_market.quantity_unit})', fontsize=16, fontweight='bold')
        ax_right.set_ylabel(f'Price ({original_market.price_unit})', fontsize=16, fontweight='bold')
        ax_right.set_title('Equilibrium Comparison', fontsize=16, fontweight='bold')
        ax_right.legend(loc='best', fontsize=12, framealpha=0.9)
        ax_right.grid(True, alpha=0.3)
        ax_right.set_xlim(left=0)
        ax_right.set_ylim([p_min, p_max])

    plt.tight_layout()

    return fig


def plot_market_surplus(market: SupplyDemand,
                        price: Optional[float] = None,
                        show_consumer_surplus: bool = True,
                        show_producer_surplus: bool = True,
                        show_demand_curve: bool = True,
                        show_supply_curve: bool = True,
                        figsize: Tuple[float, float] = (10, 7),
                        title: Optional[str] = None) -> plt.Figure:
    """
    Create a supply and demand plot with shaded surplus regions.

    Parameters
    ----------
    market : SupplyDemand
        Market object containing supply/demand parameters
    price : float, optional
        Price level at which to calculate surplus. If None, uses equilibrium price.
    show_consumer_surplus : bool, default=True
        Whether to shade and label consumer surplus area
    show_producer_surplus : bool, default=True
        Whether to shade and label producer surplus area
    figsize : tuple, default=(10, 7)
        Figure size (width, height) in inches
    title : str, optional
        Custom title. If None, uses default.

    Returns
    -------
    matplotlib.figure.Figure
        The created figure
    """
    # Create figure
    fig, ax = plt.subplots(figsize=figsize)

    # Use equilibrium price if not specified
    if price is None:
        price, quantity = market.equilibrium()
    else:
        # At specified price, use quantity demanded (consumer perspective)
        quantity = min(market.quantity_supplied(price), market.quantity_demanded(price))

    # Determine price range
    p_eq, q_eq = market.equilibrium()
    p_min = 0
    p_max = p_eq * 1.8

    prices_full = np.linspace(p_min, p_max, 500)

    # Calculate supply and demand curves
    qs_full = market.quantity_supplied(prices_full)
    qd_full = market.quantity_demanded(prices_full)


    if show_supply_curve:
        # Plot supply curve
        ax.plot(qs_full, prices_full, linewidth=3.0, color=UTM_BLUE, label='Supply', zorder=2)

    if show_demand_curve:
        # Plot demand curve
        ax.plot(qd_full, prices_full, linewidth=3.0, color=UTM_ORANGE, label='Demand', zorder=2)
    
    # Add horizontal price line (using data coordinates)
    ax.hlines(y=price, xmin=0, xmax=q_eq, color='black', linestyle=':', linewidth=3, alpha=0.7, zorder=3)
    # ax.text(quantity * 0.05, price * 1.02, f'Price = {price:.1f}',
    #        fontsize=9, va='bottom', color='darkgreen', fontweight='bold')
    
    ax.text(q_eq * 1.15, p_eq * 1.01, f'Price = {p_eq:.1f}',
           fontsize=14, va='bottom', color='black', fontweight='bold')
        
    ax.text(q_eq * 1.02, p_eq * 0.05, f'Quantity = {q_eq:.1f}',
           fontsize=14, va='bottom', color='black', fontweight='bold')

    # Calculate choke prices (where curves hit the axes)
    # Demand choke price: where Qd = 0
    p_choke_demand = market.demand_intercept / market.demand_slope
    # Supply choke price: where Qs = 0
    p_choke_supply = -market.supply_intercept / market.supply_slope

    # Shade consumer surplus (area above price, below demand)
    if show_consumer_surplus:
        # Consumer surplus region: from current price up to choke price
        cs_prices = np.linspace(price, min(p_choke_demand, p_max), 200)
        cs_quantities = market.quantity_demanded(cs_prices)

        # Fill area between price line and demand curve
        ax.fill_betweenx(cs_prices, 0, cs_quantities,
                        alpha=0.25, color='skyblue', label='Consumer Surplus', zorder=0)

        # Calculate and annotate consumer surplus value
        # CS = 0.5 * (P_choke - P_market) * Q_market
        cs_value = 0.5 * (p_choke_demand - price) * quantity

        # Position label in middle of shaded region
        cs_label_p = (price + p_choke_demand) / 2
        cs_label_q = quantity / 2
        ax.text(cs_label_q, price * 1.05, f'CS = {cs_value:.1f}',
               fontsize=14, ha='center', va='center', fontweight='bold',
               bbox=dict(boxstyle='round', facecolor='skyblue', alpha=0.6))

    # Shade producer surplus (area below price, above supply)
    if show_producer_surplus:
        # Producer surplus region: from supply choke price up to current price
        ps_prices = np.linspace(max(p_choke_supply, p_min), price, 200)
        ps_quantities = market.quantity_supplied(ps_prices)

        # Fill area between supply curve and price line
        ax.fill_betweenx(ps_prices, 0, ps_quantities,
                        alpha=0.25, color='lightgreen', label='Producer Surplus', zorder=0)

        # Calculate and annotate producer surplus value
        # PS = 0.5 * (P_market - P_choke) * Q_market
        ps_value = 0.5 * (price - p_choke_supply) * quantity

        # Position label in middle of shaded region
        ps_label_p = (price + p_choke_supply) / 2
        ps_label_q = quantity / 2
        ax.text(ps_label_q, price * 0.95, f'PS = {ps_value:.1f}',
               fontsize=14, ha='center', va='center', fontweight='bold',
               bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.6))

    # Mark equilibrium point
    ax.plot(quantity, price, 'o', markersize=10, color='black', zorder=5)

    # Add vertical line at equilibrium quantity
    ax.vlines(x=q_eq, ymin=0, ymax=p_eq, color='black', linestyle='--', alpha=0.7, linewidth=2, zorder=1)

    # Configure axes
    ax.set_xlabel(f'Quantity ({market.quantity_unit})', fontsize=16, fontweight='bold')
    ax.set_ylabel(f'Price ({market.price_unit})', fontsize=16, fontweight='bold')

    if title is None:
        title = f'Market Surplus: {market.commodity}'
    ax.set_title(title, fontsize=20, fontweight='bold')

    # Add legend
    ax.legend(loc='best', fontsize=12, framealpha=0.9)

    # Enable grid
    ax.grid(True, alpha=0.3)

    # Set axis limits
    ax.set_xlim(left=0)
    ax.set_ylim([p_min, p_max])

    plt.tight_layout()

    return fig


def plot_excess_demand_and_supply(market: SupplyDemand,
                                  excess_type: str = 'supply',
                                  price_level: Optional[float] = None,
                                  figsize: Tuple[float, float] = (10, 7),
                                  price_range: Optional[Tuple[float, float]] = None,
                                  title: Optional[str] = None) -> plt.Figure:
    """
    Show excess supply or excess demand at a given price level.

    Parameters
    ----------
    market : SupplyDemand
        Market object containing supply/demand parameters
    excess_type : str, default='supply'
        'supply' to show excess supply (price above equilibrium) or
        'demand' to show excess demand (price below equilibrium)
    price_level : float, optional
        Price at which to illustrate the excess. If None, defaults to
        1.25x equilibrium price (excess supply) or 0.75x (excess demand).
    figsize : tuple, default=(10, 7)
        Figure size (width, height) in inches
    price_range : tuple, optional
        (min_price, max_price) for y-axis. If None, auto-determined.
    title : str, optional
        Custom title. If None, uses 'Excess Supply' or 'Excess Demand'.

    Returns
    -------
    matplotlib.figure.Figure
        The created figure
    """
    # Compute equilibrium
    p_eq, _ = market.equilibrium()

    # Auto-calculate price_level if not provided
    if price_level is None:
        if excess_type.lower() == 'supply':
            price_level = p_eq * 1.25
        else:
            price_level = p_eq * 0.75

    # Determine price range for the plot
    if price_range is None:
        p_min = 0
        p_max = max(price_level, p_eq) * 1.5
    else:
        p_min, p_max = price_range

    # Generate curve data
    prices = np.linspace(p_min, p_max, 500)
    qs = market.quantity_supplied(prices)
    qd = market.quantity_demanded(prices)

    fig, ax = plt.subplots(figsize=figsize)

    # Plot supply and demand curves
    ax.plot(qs, prices, linewidth=3.0, color=UTM_BLUE, zorder=2)
    ax.plot(qd, prices, linewidth=3.0, color=UTM_ORANGE, zorder=2)

    # Label curves at their upper ends (textbook style, no legend)
    qs_top = market.quantity_supplied(p_max)
    qd_top = market.quantity_demanded(p_max)
    ax.text(qs_top, p_max * 0.97, 'Supply\ncurve',
            fontsize=12, ha='center', va='top', color=UTM_BLUE, fontweight='bold')
    # Only label demand if it's still visible at the top of the range
    if qd_top > 0:
        ax.text(qd_top, p_max * 0.97, 'Demand\ncurve',
                fontsize=14, ha='center', va='top', color=UTM_BLUE, fontweight='bold')
    # Compute quantities at the specified price
    qs_at_price = market.quantity_supplied(price_level)
    qd_at_price = market.quantity_demanded(price_level)
    q_left = min(qs_at_price, qd_at_price)
    q_right = max(qs_at_price, qd_at_price)

    # Horizontal dotted line at price_level
    ax.hlines(y=price_level, xmin=0, xmax=q_right,
              color='black', linestyle=':', linewidth=2, alpha=0.7, zorder=3)

    # Vertical dotted lines from price_level down to x-axis
    ax.vlines(x=qs_at_price, ymin=0, ymax=price_level,
              color='black', linestyle=':', linewidth=2, alpha=0.7, zorder=3)
    ax.vlines(x=qd_at_price, ymin=0, ymax=price_level,
              color='black', linestyle=':', linewidth=2, alpha=0.7, zorder=3)

    # Annotation style for quantity labels
    box_style = dict(boxstyle='round,pad=0.3', facecolor='lightgray', alpha=0.8, edgecolor='gray')
    y_offset = (p_max - p_min) * 0.08  # vertical offset for label placement

    # "Quantity Demanded" annotation with arrow to intersection
    ax.annotate('Quantity\nDemanded',
                xy=(qd_at_price, price_level),
                xytext=(qd_at_price, price_level + y_offset),
                fontsize=14, ha='center', va='bottom',
                bbox=box_style,
                arrowprops=dict(arrowstyle='->', lw=1.5, color='gray'))

    # "Quantity Supplied" annotation with arrow to intersection
    ax.annotate('Quantity\nSupplied',
                xy=(qs_at_price, price_level),
                xytext=(qs_at_price, price_level + y_offset),
                fontsize=14, ha='center', va='bottom',
                bbox=box_style,
                arrowprops=dict(arrowstyle='->', lw=1.5, color='gray'))

    # Double-headed arrow spanning the excess gap
    is_excess_supply = excess_type.lower() == 'supply'
    label_text = 'Excess\nSupply' if is_excess_supply else 'Excess\nDemand'

    # Place the arrow along the price line between the two quantities
    mid_q = (q_left + q_right) / 2
    ax.annotate('', xy=(q_right, price_level), xytext=(q_left, price_level),
                arrowprops=dict(arrowstyle='<->', lw=2.0, color='black'),
                zorder=4)

    # Centered label for excess type
    # Position slightly above or below the price line depending on scenario
    label_y = price_level + y_offset * 2.5 if is_excess_supply else price_level - y_offset * 1.5
    ax.text(mid_q, label_y, label_text,
            fontsize=13, ha='center', va='center', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='none', alpha=0.9))

    # Axis labels
    ax.set_xlabel(f'Quantity ({market.quantity_unit})', fontsize=16, fontweight='bold')
    ax.set_ylabel(f'Price ({market.price_unit})', fontsize=16, fontweight='bold')

    # Title
    if title is None:
        title = 'Excess Supply' if is_excess_supply else 'Excess Demand'
    ax.set_title(title, fontsize=20, fontweight='bold')

    ax.grid(True, alpha=0.5)
    ax.set_xlim(left=0)
    ax.set_ylim([p_min, p_max])

    plt.tight_layout()

    return fig


def plot_elasticity_comparison(curve_type: str,
                                inelastic_market: SupplyDemand,
                                elastic_market: SupplyDemand,
                                p1: float,
                                p2: Optional[float] = None,
                                shifted_market: Optional[SupplyDemand] = None,
                                figsize: Tuple[float, float] = (10, 7),
                                price_range: Optional[Tuple[float, float]] = None,
                                title: Optional[str] = None,
                                ax: Optional[plt.Axes] = None) -> plt.Figure:
    """
    Compare elastic vs. inelastic curves on the same graph.

    Shows how a price change produces different quantity responses depending
    on the elasticity of the curve. Both elasticity curves must intersect
    at p1 (caller's responsibility to set up the markets accordingly).

    Can operate in two modes:
    1. **Manual price mode** (p2 provided): draws reference lines at a
       single p2 level, showing different quantity responses.
    2. **Shift mode** (shifted_market provided): plots the original and
       shifted opposite curve, then computes separate new-equilibrium
       prices for each elasticity curve. For example, when comparing
       demand elasticities, provide the original supply via
       inelastic_market/elastic_market supply params and a shifted supply
       via shifted_market.

    Parameters
    ----------
    curve_type : str
        'demand' or 'supply' — which curve type to compare elasticities of
    inelastic_market : SupplyDemand
        Market whose compared curve is steep (inelastic).
        Its opposite curve is used as the original (S1 or D1) when
        shifted_market is provided.
    elastic_market : SupplyDemand
        Market whose compared curve is shallow (elastic)
    p1 : float
        Initial price where both elasticity curves intersect
    p2 : float, optional
        New price level (manual mode). Ignored when shifted_market is set.
    shifted_market : SupplyDemand, optional
        Market after the opposite curve has shifted. When provided, its
        opposite curve is plotted as S2/D2 and new equilibrium prices are
        computed automatically.
    figsize : tuple, default=(10, 7)
        Figure size (width, height) in inches
    price_range : tuple, optional
        (min_price, max_price) for y-axis. If None, auto-determined.
    title : str, optional
        Custom title. If None, auto-generated from curve_type.
    ax : matplotlib.axes.Axes, optional
        Existing axes to plot on. If None, creates new figure.

    Returns
    -------
    matplotlib.figure.Figure
        The created or modified figure
    """
    # Create figure if not provided
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.get_figure()

    is_demand = curve_type.lower() == 'demand'
    use_shift = shifted_market is not None

    # Validate inputs
    if not use_shift and p2 is None:
        raise ValueError("Either p2 or shifted_market must be provided.")

    # --- Compute initial intersection quantity at p1 ---
    if is_demand:
        q1 = inelastic_market.quantity_demanded(p1)
    else:
        q1 = inelastic_market.quantity_supplied(p1)

    # --- Shift mode: compute new equilibrium prices from shifted curve ---
    if use_shift:
        # Build full markets pairing each elasticity curve with the shifted opposite curve
        if is_demand:
            # Inelastic demand + shifted supply
            inel_shifted = SupplyDemand(
                shifted_market.supply_intercept, shifted_market.supply_slope,
                inelastic_market.demand_intercept, inelastic_market.demand_slope)
            # Elastic demand + shifted supply
            elas_shifted = SupplyDemand(
                shifted_market.supply_intercept, shifted_market.supply_slope,
                elastic_market.demand_intercept, elastic_market.demand_slope)
        else:
            # Inelastic supply + shifted demand
            inel_shifted = SupplyDemand(
                inelastic_market.supply_intercept, inelastic_market.supply_slope,
                shifted_market.demand_intercept, shifted_market.demand_slope)
            # Elastic supply + shifted demand
            elas_shifted = SupplyDemand(
                elastic_market.supply_intercept, elastic_market.supply_slope,
                shifted_market.demand_intercept, shifted_market.demand_slope)

        p2_inelastic, q2_inelastic = inel_shifted.equilibrium()
        p2_elastic, q2_elastic = elas_shifted.equilibrium()
    else:
        # Manual mode: single p2 for both curves
        p2_inelastic = p2
        p2_elastic = p2
        if is_demand:
            q2_inelastic = inelastic_market.quantity_demanded(p2)
            q2_elastic = elastic_market.quantity_demanded(p2)
        else:
            q2_inelastic = inelastic_market.quantity_supplied(p2)
            q2_elastic = elastic_market.quantity_supplied(p2)

    # --- Determine price range ---
    if price_range is None:
        p_min = 0
        p_max = max(p1, p2_inelastic, p2_elastic) * 1.8
    else:
        p_min, p_max = price_range

    prices = np.linspace(p_min, p_max, 500)

    # --- Plot the opposite curves (S1/S2 or D1/D2) when in shift mode ---
    if use_shift:
        # Abbreviation for the opposite curve type
        other_abbrev = 'S' if is_demand else 'D'
        other_color = UTM_ORANGE

        if is_demand:
            q_other_orig = inelastic_market.quantity_supplied(prices)
            q_other_shift = shifted_market.quantity_supplied(prices)
        else:
            q_other_orig = inelastic_market.quantity_demanded(prices)
            q_other_shift = shifted_market.quantity_demanded(prices)

        # Original opposite curve (UTM Orange, solid)
        ax.plot(q_other_orig, prices, linewidth=3.0, color=other_color, zorder=1)
        # Shifted opposite curve (UTM Orange, slightly lighter)
        ax.plot(q_other_shift, prices, linewidth=3.0, color=other_color, alpha=0.6, zorder=1)

        # Label the opposite curves where they are clearly on-plot.
        # Supply curves (opposite of demand) extend upward — label near top.
        # Demand curves (opposite of supply) slope down — label at a lower
        # price so the quantity is still well within the visible area.
        other_label_bbox = dict(boxstyle='round,pad=0.2', facecolor='white',
                                edgecolor='none', alpha=0.85)
        if is_demand:
            # Supply curves go up-right — label near top of price range
            label_p_other = p_max * 0.92
            q_orig_label = inelastic_market.quantity_supplied(label_p_other)
            q_shift_label = shifted_market.quantity_supplied(label_p_other)
        else:
            # Demand curves go down-right — label near upper portion of each
            # curve where Q is still positive. Use the choke price (Q=0) as
            # the ceiling and back off to keep labels on-plot.
            p_choke_orig = inelastic_market.demand_intercept / inelastic_market.demand_slope
            p_choke_shift = shifted_market.demand_intercept / shifted_market.demand_slope
            label_p_orig = p_choke_orig * 0.85
            label_p_shift = p_choke_shift * 0.85
            q_orig_label = inelastic_market.quantity_demanded(label_p_orig)
            q_shift_label = shifted_market.quantity_demanded(label_p_shift)

        # Use per-curve label prices for demand; shared price for supply
        lp_orig = label_p_orig if not is_demand else label_p_other
        lp_shift = label_p_shift if not is_demand else label_p_other

        ax.text(q_orig_label, lp_orig, rf'${other_abbrev}_1$',
                fontsize=14, ha='center', va='bottom', fontweight='bold',
                color=other_color, zorder=4, bbox=other_label_bbox)
        ax.text(q_shift_label, lp_shift, rf'${other_abbrev}_2$',
                fontsize=14, ha='center', va='bottom', fontweight='bold',
                color=other_color, zorder=4, bbox=other_label_bbox)

    # --- Plot the elasticity curves (demand or supply) ---
    if is_demand:
        q_inelastic = inelastic_market.quantity_demanded(prices)
        q_elastic = elastic_market.quantity_demanded(prices)
    else:
        q_inelastic = inelastic_market.quantity_supplied(prices)
        q_elastic = elastic_market.quantity_supplied(prices)

    ax.plot(q_inelastic, prices, linewidth=3.0, color=UTM_BLUE, zorder=2)
    ax.plot(q_elastic, prices, linewidth=3.0, color=UTM_BLUE, zorder=2)

    # --- Label the elasticity curves ---
    # Place labels where curves are well separated to avoid overlap.
    # Demand curves diverge at low prices; supply curves diverge at high prices.
    # Use different heights for each label for extra separation.
    if is_demand:
        # Lower prices → more separation; inelastic label higher, elastic lower
        inel_label_p = p_max * 0.85
        elas_label_p = p_max * 0.85
        q_inel_at_label = inelastic_market.quantity_demanded(inel_label_p)
        q_elas_at_label = elastic_market.quantity_demanded(elas_label_p)
    else:
        # Higher prices → more separation; elastic label higher, inelastic lower
        inel_label_p = p_max * 0.85
        elas_label_p = p_max * 0.85
        q_inel_at_label = inelastic_market.quantity_supplied(inel_label_p)
        q_elas_at_label = elastic_market.quantity_supplied(elas_label_p)

    inelastic_label = f'Inelastic\n{curve_type.lower()}'
    elastic_label = f'Elastic\n{curve_type.lower()}'

    label_bbox = dict(boxstyle='round,pad=0.3', facecolor='white',
                      edgecolor='none', alpha=0.85)
    ax.text(q_inel_at_label, inel_label_p, inelastic_label,
            fontsize=12, ha='center', va='bottom', fontweight='bold',
            color=UTM_ORANGE, zorder=4, bbox=label_bbox)
    ax.text(q_elas_at_label, elas_label_p, elastic_label,
            fontsize=12, ha='center', va='bottom', fontweight='bold',
            color=UTM_ORANGE, zorder=4, bbox=label_bbox)

    # --- Reference lines at p1 ---
    ax.hlines(y=p1, xmin=0, xmax=q1,
              color='black', linestyle=':', linewidth=2, alpha=0.7, zorder=3)
    ax.vlines(x=q1, ymin=0, ymax=p1,
              color='black', linestyle=':', linewidth=2, alpha=0.7, zorder=3)

    # Mark intersection point
    ax.plot(q1, p1, 'o', markersize=8, color='black', zorder=5)

    # --- Reference lines at p2 ---
    if use_shift:
        # Inelastic equilibrium reference lines (dotted)
        ax.hlines(y=p2_inelastic, xmin=0, xmax=q2_inelastic,
                  color='black', linestyle=':', linewidth=2, alpha=0.7, zorder=3)
        ax.vlines(x=q2_inelastic, ymin=0, ymax=p2_inelastic,
                  color='black', linestyle=':', linewidth=2, alpha=0.7, zorder=3)

        # Elastic equilibrium reference lines (dashed)
        ax.hlines(y=p2_elastic, xmin=0, xmax=q2_elastic,
                  color='black', linestyle='--', linewidth=2, alpha=0.7, zorder=3)
        ax.vlines(x=q2_elastic, ymin=0, ymax=p2_elastic,
                  color='black', linestyle='--', linewidth=2, alpha=0.7, zorder=3)

        # Mark new equilibrium points
        ax.plot(q2_inelastic, p2_inelastic, 'o', markersize=8, color='black', zorder=5)
        ax.plot(q2_elastic, p2_elastic, 'o', markersize=8, color='black', zorder=5)
    else:
        # Single p2 with lines to both quantity values
        q2_max = max(q2_inelastic, q2_elastic)
        ax.hlines(y=p2, xmin=0, xmax=q2_max,
                  color='black', linestyle='--', linewidth=2, alpha=0.7, zorder=3)
        ax.vlines(x=q2_inelastic, ymin=0, ymax=p2,
                  color='black', linestyle='--', linewidth=2, alpha=0.7, zorder=3)
        ax.vlines(x=q2_elastic, ymin=0, ymax=p2,
                  color='black', linestyle='--', linewidth=2, alpha=0.7, zorder=3)

    # --- Symbolic axis tick labels ---
    curve_abbrev = 'D' if is_demand else 'S'
    q_ticks = [q1, q2_inelastic, q2_elastic]
    q_labels = [r'$Q_1$',
                rf'$Q_{{2,I{curve_abbrev}}}$',
                rf'$Q_{{2,E{curve_abbrev}}}$']

    if use_shift:
        p_ticks = [p2_inelastic, p2_elastic, p1]
        p_labels_list = [rf'$P_{{2,I{curve_abbrev}}}$',
                         rf'$P_{{2,E{curve_abbrev}}}$',
                         r'$P_1$']
    else:
        p_ticks = [p1, p2_inelastic]
        p_labels_list = [r'$P_1$', r'$P_2$']

    ax.set_xticks(q_ticks)
    ax.set_xticklabels(q_labels, fontsize=14)
    ax.set_yticks(p_ticks)
    ax.set_yticklabels(p_labels_list, fontsize=14)

    # Axis labels
    ax.set_xlabel('Quantity', fontsize=16, fontweight='bold')
    ax.set_ylabel('Price', fontsize=16, fontweight='bold')

    # Title
    if title is None:
        title = f'Elastic vs. Inelastic {curve_type.capitalize()}'
    ax.set_title(title, fontsize=20, fontweight='bold')

    ax.grid(True, alpha=0.3)
    ax.set_xlim(left=0)
    ax.set_ylim([p_min, p_max])

    plt.tight_layout()

    return fig