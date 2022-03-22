-- Neue Bruttoleistung pro Kalenderwoche aller Windeinheiten an Land seit Beginn 2022.
with ProWoche as (
  select
    strftime("%Y-%W", Inbetriebnahmedatum) as Kalenderwoche,
    sum(Bruttoleistung) as BruttoleistungKW
  from
    EinheitWind
  where
    Inbetriebnahmedatum >= "2022-01-01"
    and Lage = (
      select
        Id
      from
        Katalogwert k
      where
        k.Wert = "Windkraft an Land"
    )
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
