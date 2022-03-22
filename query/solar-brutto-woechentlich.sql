-- Neue Bruttoleistung pro Kalenderwoche aller Photovoltaikeinheiten seit Beginn 2022.
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
)
select
  json_group_object(
    Kalenderwoche,
    cast(
      printf("%.03f", BruttoleistungKW) as real
    )
  )
from
  ProWoche
