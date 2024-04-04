# Tributary
Backend infrastructure for Ford's sensor streaming system. This codebase contains a Flask server which records data to a Redis database, and exposes two endpoints. The /record endpoint is periodically called by embedded sensors within a vehicle to post data to the database.
