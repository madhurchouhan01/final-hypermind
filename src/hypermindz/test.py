from crewai_tools import tool


def calculate_channel_metrics(input_data: dict) -> dict:
    """
    Calculate investment metrics for media channels using CPM and targeting assumptions.

    Parameters:
    -----------
    input_data : dict
        {
            "total_budget": float,
            "audience_size": int,
            "adult_pop": int,
            "flight": int
        }

    Returns:
    --------
    dict :
        - List of updated channel metrics
        - Summary with gross and target reach estimates
    """

    channels_data = {
        "channels": [
            {"percent_allocation": 15, "channel": "OOH", "cpm": 15, "target_comp_multiplier": 3},
            {"percent_allocation": 0, "channel": "Linear TV", "cpm": 25, "target_comp_multiplier": 3},
            {"percent_allocation": 0, "channel": "Print", "cpm": 35, "target_comp_multiplier": 3},
            {"percent_allocation": 10, "channel": "CTV", "cpm": 35, "target_comp_multiplier": 40},
            {"percent_allocation": 10, "channel": "OLV", "cpm": 20, "target_comp_multiplier": 40},
            {"percent_allocation": 10, "channel": "Digital Display", "cpm": 12, "target_comp_multiplier": 20},
            {"percent_allocation": 15, "channel": "Integrated Partnerships", "cpm": 75, "target_comp_multiplier": 5},
            {"percent_allocation": 10, "channel": "Audio: host-read", "cpm": 60, "target_comp_multiplier": 5},
            {"percent_allocation": 10, "channel": "Audio: targeted", "cpm": 30, "target_comp_multiplier": 40},
            {"percent_allocation": 20, "channel": "Social: targeted", "cpm": 25, "target_comp_multiplier": 50}
        ]
    }

    sum_gross_imps = 0
    sum_target_imps = 0
    sum_gross_imps_freq = 15
    sum_target_imps_freq = 25
    total_budget_per_month = 0

    gross_imps_freq = 0
    target_imps_freq = 0
    updated_channel_parameters = []

    for channel_data in channels_data['channels']:
        percent_alloc = channel_data['percent_allocation'] / 100

        channel = channel_data["channel"]
        cpm = channel_data['cpm']
        target_multiplier = channel_data['target_comp_multiplier']

        monthly_budget = (input_data["total_budget"] * percent_alloc) / input_data["flight"]
        target_comp = input_data["audience_size"] / input_data["adult_pop"]
        target_audience_comp = target_comp * target_multiplier * 100
        gross_imps = (monthly_budget / cpm) * 1000
        target_imps = target_audience_comp * gross_imps

        # if monthly_budget <= 1_000_000:
        #     gross_imps_freq = 3
        #     target_imps_freq = 5
        # elif 1_000_000 <= monthly_budget <= 2_000_000:
        #     gross_imps_freq = 6
        #     target_imps_freq = 25


        sum_gross_imps += gross_imps
        sum_target_imps += target_imps
        sum_gross_imps_freq += gross_imps_freq
        sum_target_imps_freq += target_imps_freq
        total_budget_per_month += monthly_budget

        updated_channel_parameters.append({
            "percent_allocation": percent_alloc,
            "channel": channel,
            "cpm": cpm,
            "target_multiplier": target_multiplier,
            "monthly_budget": monthly_budget,
            "target_comp": target_comp,
            "target_audience_comp": target_audience_comp,
            "gross_imps": gross_imps,
            "target_imps": target_imps,
        })

    gross_unique_reach = round(sum_gross_imps / sum_gross_imps_freq, 2)
    target_unique_reach = round(sum_target_imps / sum_target_imps_freq, 2)
    gross_reach_percent = round((gross_unique_reach / input_data["adult_pop"]) * 100, 2)
    target_reach_percent = round((target_unique_reach / input_data["audience_size"]) * 100,2)

    return {
        "channels": updated_channel_parameters,
        "summary": {
            "gross_unique_reach": gross_unique_reach,
            "target_unique_reach": target_unique_reach,
            "gross_reach_percent": gross_reach_percent,
            "target_reach_percent": target_reach_percent,
            "total_budget_per_month" : total_budget_per_month,
        }
    }
result = calculate_channel_metrics(
    {
  "audience_size": 2000000,
  "total_budget": 10000000,
  "flight": 10,
  "adult_pop" :   258000000
}
)

print(result)