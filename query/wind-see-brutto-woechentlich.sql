-- Neue Bruttoleistung pro Kalenderwoche aller Windeinheiten auf See seit Beginn 2022.
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
        k.Wert = "Windkraft auf See"
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
