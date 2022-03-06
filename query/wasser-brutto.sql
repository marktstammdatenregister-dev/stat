-- Bruttoleistung aller Wassereinheiten, die aktuell in Betrieb sind.
select
  sum(Bruttoleistung)
from
  EinheitWasser
where
  EinheitBetriebsstatus = 35
  and EinheitSystemstatus = 472
