# Ericai

- https://eteamspace.internal.ericsson.com/display/BFSTOS/EricAI

## Installation of Ericai client

```
pip install git+ssh://git@gitlab.internal.ericsson.com/sw-tech/ericai-client.git
```

To test connectivity, run:

```
ericai --ericsson-test-connectivity
```

Test list all models:
```
ericai api models.list
```

## How to run test script

1. Get access token:
```
ericai --ericsson-access-token
```
(You may be requested to login again using a QR code, or the link https://microsoft.com/devicelogin. Enter the code shown on the screen to authenticate the device)

2. Set the access token as an environment variable:
```
export ERICAI_ACCESS_TOKEN=<ACCESS_TOKEN>
```
3. Run ericai api test script:
```
 python test-ericai-deepseek-r1.py
```

## Example Code

https://gitlab.internal.ericsson.com/sw-tech/ericai-client/-/blob/master/example/example.py?ref_type=heads
