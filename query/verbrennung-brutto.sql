-- Bruttoleistung aller Verbrennungseinheiten, die aktuell in Betrieb sind.
select
  sum(Bruttoleistung)
from
  EinheitVerbrennung
where
  EinheitBetriebsstatus = 35
  and EinheitSystemstatus = 472
