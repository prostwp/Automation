keys = {
    "general_outlook": ["{{ 'space_general_outlook' | trans | raw }}"],
    "global_trend": [
        "{{ 'space_mlvl_outl_has_been_trading_in_bullbear_trend_within_last_day' | trans ({ '[symbol]': symbol, '[bullish_bearish]': 'space_trend_bullish' | trans }) | raw }}",
        "{{ 'space_mlvl_outl_has_been_trading_in_bullbear_trend_within_last_day' | trans ({ '[symbol]': symbol, '[bullish_bearish]': 'space_trend_bearish' | trans }) | raw }}",
        "{{ 'space_mlvl_outl_has_been_trading_in_sideways_market_within_last_day' | trans ({ '[symbol]': symbol }) | raw }}"
    ],
    "local_trend": [
        "{{ 'space_mlvl_outl_has_been_trading_in_bullbear_trend_for_the_last_couple_hors' | trans ({ '[symbol]': symbol, '[bullish_bearish]': 'space_trend_bullish' | trans }) | raw }}",
        "{{ 'space_mlvl_outl_has_been_trading_in_bullbear_trend_for_the_last_couple_hors' | trans ({ '[symbol]': symbol, '[bullish_bearish]': 'space_trend_bearish' | trans }) | raw }}",
        "{{ 'space_mlvl_outl_has_been_trading_in_sideways_market_for_couple_hours' | trans ({ '[symbol]': symbol }) | raw }}"
    ],
    "display_pattern": [
        "{{ 'space_market_overview_exp_now_price_displays_the_pattern' | trans ({ '[pattern]': 'Wedge' }) | raw }}"],
    "buy_rebound": [
        "{{ 'space_figures_exp_if_price_rebounds_from_lower_border_or_confirms_breakout_from_upper_border_opening_buy_order' | trans ({ '[pattern]': 'Wedge' }) | raw }}"],
    "sell_rebound": [
        "{{ 'space_figures_exp_if_price_rebounds_from_upper_border_or_confirms_breakout_from_lower_border_opening_sell_order' | trans ({ '[pattern]': 'Wedge' }) | raw }}"],
    "triangle_titlte": [
        "{{ 'space_figures_title_formed_pattern' | trans ({ '[symbol]': symbol, '[pattern]': 'Triangle' }) | raw }}", ],
    "title": [
        "{{ 'space_patterns_title_formed_bullish_pattern' | trans ({ '[symbol]': symbol, '[pattern]': 'Wedge' }) | raw }}",
        "{{ 'space_patterns_title_formed_bearish_pattern' | trans ({ '[symbol]': symbol, '[pattern]': 'Wedge' }) | raw }}"],
    "in_case": [
        "{{ 'space_figures_exp_in_case_of_breakout_or_retest_of_neckline_open_buysell_order_place_sl_behind_right_shoulder' | trans ({ '[buy_sell]': 'space_order_buy' | trans }) | raw }}",
        "{{ 'space_figures_exp_in_case_of_breakout_or_retest_of_neckline_open_buysell_order_place_sl_behind_right_shoulder' | trans ({ '[buy_sell]': 'space_order_sell' | trans }) | raw }}"],
    "no_news":
        ["{{ 'space_upcoming_news_will_not_influence_your_orders' | trans | raw }}"],
    "neckline": [
        "{{ 'space_figures_exp_in_case_of_breakout_or_retest_of_neckline_open_buysell_order_place_sl_behind_right_shoulder' | trans ({ '[buy_sell]': 'space_order_sell' | trans }) | raw }}",
        "{{ 'space_figures_exp_in_case_of_breakout_or_retest_of_neckline_open_buysell_order_place_sl_behind_right_shoulder' | trans ({ '[buy_sell]': 'space_order_buy' | trans }) | raw }}"],
    "drop_rise": ["{{ 'space_patterns_descr_now_price_is_ready_to_drop' | trans | raw }}",
                  "{{ 'space_patterns_descr_now_price_is_ready_to_rise' | trans | raw }}"],
    "fundamental_factors":
        ["{{ 'space_fundamental_factors' | trans | raw }}"],
    "friday": ["{{ 'space_factors_traders_may_close_positions_on_friday' | trans }}"]
}