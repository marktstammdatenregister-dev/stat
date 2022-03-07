-- Anzahl aller Wassereinheiten, die aktuell in Betrieb sind.
select
  count(EinheitMastrNummer)
from
  EinheitWasser
where
  EinheitBetriebsstatus = 35
  and EinheitSystemstatus = 472
