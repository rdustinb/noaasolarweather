This directory contains the results of the profiling work done on the Space
Weather application. It will help in the rearchitecting of the application to
be more efficient and hopefully speed up the Application.

The command run to generate the Profile report is:

```
python3.4 -m cProfile -s "cumtime" src/SpaceWeather.py > profile/original_profile.log
```