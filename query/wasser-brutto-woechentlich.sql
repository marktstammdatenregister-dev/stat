-- Neue Bruttoleistung pro Kalenderwoche aller Wasserkrafteinheiten seit Beginn 2022.
with ProWoche as (
  select
    strftime("%Y-%W", Inbetriebnahmedatum) as Kalenderwoche,
    sum(Bruttoleistung) as BruttoleistungKW
  from
    EinheitWasser
  where
    Inbetriebnahmedatum >= "2022-01-01"
  group by
    Kalenderwoche
)
select
  json_group_object(
    Kalenderwoche,
    round(BruttoleistungKW, 3)
  )
from
  ProWoche
