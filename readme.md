# Backend

The backend of this project is a flask webserver. The source of the data is [The Daily Racing Form](https://www.drf.com/data-services) without which it is impossible to run a useful local version (TODO: add sample data files and sample prediction model so that backend can run as a demo).

## Domain Issues

The domain of horseracing data is fraught with issues. Horseracing data is sourced from a company like the aforementioned DRF, which all have very poor tooling for software bettors. Their primary business is tailored to readers and button-clickers. This leads to issues like trying to match a horse from a previous race with a name like `Dan's Legacy` with the same horse in the current race with a name like `dans legacy`. Simple things like this must be addressed by an app that wants to avoid garbage in garbage out. Thus, I use a robust ETL layer and store data in my own postgres database which I can then query for use in a machine learning model or an API and trust the output.

There is another interesting issue with horseracing, which is that there is a temporal element to them. The live odds at the time of racing are an input to my model, and to many horseracing prediction models. But you can only access the true live odds moments before the race begins. A horse may be entered into a race, then drop out as a "scratch" before the race begins. Or a race may be scheduled for a certain surface, then be changed due to rain. These variables are up in the air until the last minute, and are not adequately covered by the available data sources. So it introduces a requirement on this app to support user-input to quickly and ergonomically update the inputs to the model on the fly.

## ETL

Pre-race info comes from DRF. I make use of an undocumented API to export files and upload them to S3. From S3, the files are downloaded and sent to processing via [this script](https://github.com/qcomps/public-horseracing-app/blob/master/api/scripts/dataload/s3/race_day_data.py), which ultimately parses the files and stores the records in the DB.

On any given day, once the data has been processed into the DB, then the app will be able to render the data to inform the user about the day's upcoming races.

## API

Diagram of the db models:

This app uses flask and sqlalchemy to serve a json API from the database. The routes are listed in [main.py](https://github.com/qcomps/public-horseracing-app/blob/master/api/main.py).

# Client

TODO
