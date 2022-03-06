-- Bruttoleistung aller Solareinheiten, die aktuell in Betrieb sind.
select
  sum(Bruttoleistung)
from
  EinheitSolar
where
  EinheitBetriebsstatus = 35
  and EinheitSystemstatus = 472
