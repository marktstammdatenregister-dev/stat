-- Speicherkapazität aller Stromspeicher, die aktuell in Betrieb sind.
select
  sum(NutzbareSpeicherkapazitaet) as Kapazitaet
from
  AnlageStromSpeicher
where
  AnlageBetriebsstatus = 35
