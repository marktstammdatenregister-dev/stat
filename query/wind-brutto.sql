-- Bruttoleistung aller Windeinheiten, die aktuell in Betrieb sind.
select
  sum(Bruttoleistung)
from
  EinheitWind
where
  EinheitBetriebsstatus = 35
  and EinheitSystemstatus = 472
