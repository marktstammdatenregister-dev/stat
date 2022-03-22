with ProWoche as (
  select
    strftime("%Y-%W", Inbetriebnahmedatum) as Kalenderwoche,
    sum(Bruttoleistung) as BruttoleistungKW
  from
    EinheitSolar
  where
    Inbetriebnahmedatum >= "2022-01-01"
  group by
    Kalenderwoche
),
ProWocheKumulativ as (
  select
    Kalenderwoche,
    sum(BruttoleistungKW) over (
      order by
        Kalenderwoche
    ) as BruttoleistungKumulativKW
  from
    ProWoche
)
select
  json_group_object(
    Kalenderwoche,
    cast(
      printf("%.03f", BruttoleistungKumulativKW) as real
    )
  )
from
  ProWocheKumulativ
