# Python Logging Patterns

I think that this is the third time I have made a github repo about python logging.




Here is the approach I am showing in this repo:

| Approach                            | Reason
|-------------------------------------|-----------------------------------------------------------------------------------------------------------------
| Multi-destination                   | Need different information and formatting depending on where the logs are being consumed (e.g. dev vs. prod)
| Structured logs                     | Facilitates filtering and search
| Use only native python logging      | External dependencies make applications more brittle. 3rd party packages are just wrappers around native logging.
| Use DictConfig                      | MUCH easier to read and understand
| Put config in a .JSON file          | Separates configuration from code. Easier to manage different config for different environments. 
| Don't use root logger for logging   | The config of the root logger is shared by ALL loggers (even the ones in 3rd party packages)
| Use a small number of named loggers | 
|  
| 
