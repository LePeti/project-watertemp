{% set tables_to_analyze = [ref('water_temp_unique'), ref('water_temp_weekly_avg'), ref('table_stats')] %}

{%- for table in tables_to_analyze %}
    ANALYZE {{ table }};
{% endfor %}
