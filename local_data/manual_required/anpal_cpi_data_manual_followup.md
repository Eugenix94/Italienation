# ANPAL/CPI Data Manual Follow-up

Auto-generated endpoint checks:

- URL: https://dati.anpal.gov.it/api/3/action/package_list
  - status_code: None
  - ok: False
  - content_type: 
  - sample/error: HTTPSConnectionPool(host='dati.anpal.gov.it', port=443): Max retries exceeded with url: /api/3/action/package_list (Caused by NameResolutionError("HTTPSConnection(host='dati.anpal.gov.it', port=443): Failed to resolve 'dati.anpal.gov.it' ([Errno 11002] getaddrinfo failed)"))

- URL: https://dati-anpal.opendatasoft.com/api/explore/v2.1/catalog/datasets?limit=10
  - status_code: 404
  - ok: False
  - content_type: text/html
  - sample/error:  <!DOCTYPE html> <html>     <head>         <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">         <meta name="description" content="This do

- URL: https://servizi.anpal.gov.it/
  - status_code: None
  - ok: False
  - content_type: 
  - sample/error: HTTPSConnectionPool(host='servizi.anpal.gov.it', port=443): Max retries exceeded with url: / (Caused by NameResolutionError("HTTPSConnection(host='servizi.anpal.gov.it', port=443): Failed to resolve 'servizi.anpal.gov.it' ([Errno 11002] getaddrinfo failed)"))

Manual next actions:

- Verify official ANPAL open-data endpoint/domain currently in use.
- If ANPAL remains unavailable, use national labour administration alternatives and document source substitutions.
- Add CPI performance indicators (registrations, placements, placement time, ALMP participation) once endpoint is confirmed.