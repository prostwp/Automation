keys = {
    "general_outlook": ["{{ 'space_general_outlook' | trans | raw }}"],
    "title": [
        "{{ 'space_updlvl_title_is_moving_within_range' | trans ({ '[symbol]': symbol, '[number1]': 'ren1' | nf , '[number2]': 'ren2' | nf }) | raw }}"],
    "trend": [
        "{{ 'space_mlvl_outl_has_been_trading_in_bullbear_trend_within_last_day' | trans ({ '[symbol]': symbol, '[bullish_bearish]': 'space_trend_bullish' | trans }) | raw }}",
        "{{ 'space_mlvl_outl_has_been_trading_in_bullbear_trend_within_last_day' | trans ({ '[symbol]': symbol, '[bullish_bearish]': 'space_trend_bearish' | trans }) | raw }}",
        "{{ 'space_mlvl_outl_has_been_trading_in_sideways_market_within_last_day' | trans ({ '[symbol]': symbol }) | raw }}"
    ],
    "support": [
        "{{ 'space_mlvl_outl_support_resistance_level_is_now_located' | trans ({ '[support_resistance]': 'space_level_support' | trans, '[number]': 'sup1' | nf}) | raw }}",
        "{{ 'space_mlvl_outl_support_levels_are_now_located_numbers2' | trans ({ '[number1]': 'sup1' | nf, '[number2]': 'sup2' | nf, }) | raw }}",
        "{{ 'space_mlvl_outl_support_levels_are_now_located_numbers3' | trans ({ '[number1]': 'sup1' | nf, '[number2]': 'sup2' | nf, '[number3]': 'sup3' | nf }) | raw }}"],

    "resistance": [
        "{{ 'space_mlvl_outl_support_resistance_level_is_now_located' | trans ({ '[support_resistance]': 'space_level_resistance' | trans, '[number]': 'res1' | nf}) | raw }}",
        "{{ 'space_mlvl_outl_resistance_levels_are_now_located_numbers2' | trans ({ '[number1]': 'res1' | nf, '[number2]': 'res2' | nf, }) | raw }}",
        "{{ 'space_mlvl_outl_resistance_levels_are_now_located_numbers3' | trans ({ '[number1]': 'res1' | nf, '[number2]': 'res2' | nf, '[number3]': 'res3' | nf }) | raw }}"],

    "if_pair_rebound": [
        "{{ 'space_mlvl_outll_if_pair_rebounds_from_support_level_analysts_recommend_opening_buy_order' | trans | raw }}",
        "{{ 'space_mlvl_outll_if_pair_rebounds_from_resistance_level_analysts_recommend_opening_sell_order' | trans | raw }}"],

    "no_news":
        ["{{ 'space_upcoming_news_will_not_influence_your_orders' | trans | raw }}"],

    "fundamental_factors":
        ["{{ 'space_fundamental_factors' | trans | raw }}"],

    "news": [
        "{{ 'space_factors_report_will_be_released_in_few_hours' | trans ({'[country]': 'space_country_usa' | trans, '[event]': 'space_event_jobless_claims' | trans }) | raw }}",
        "{{ 'space_factors_report_will_be_released_in_few_minutes' | trans ({'[country]': 'space_country_usa' | trans, '[event]': 'space_event_jobless_claims' | trans }) | raw }}"],

    "bullish_title":
        [
            "{{ 'space_sr_title_rebounded_from_support_level_of_number' | trans ({ '[symbol]': symbol, '[number]': '1999' | nf}) | raw }}",
            "{{ 'space_sr_title_retested_support_resistance_level' | trans ({'[symbol]': symbol,'[support_resistance]': 'space_level_support' | trans, '[number]': '1999' | nf}) | raw }}"],

    "bearish_title":
        ["{{ 'space_sr_title_pulled_back_from' | trans ({ '[symbol]': symbol, '[number]': '1999' | nf}) | raw }}",
         "{{ 'space_sr_title_retested_support_resistance_level' | trans ({'[symbol]': symbol,'[support_resistance]': 'space_level_resistance' | trans, '[number]': '1999' | nf}) | raw }}"],

    "broke":
        [
            "{{ 'space_sr_title_broke_support_resistance_level' | trans ({'[symbol]': symbol, '[support_resistance]': 'space_level_support' | trans, '[number]': '1999' | nf}) | raw }}",
            "{{ 'space_sr_title_broke_support_resistance_level' | trans ({'[symbol]': symbol, '[support_resistance]': 'space_level_resistance' | trans, '[number]': '1999' | nf}) | raw }}"],
    "friday": ["{{ 'space_factors_traders_may_close_positions_on_friday' | trans }}"],
}
