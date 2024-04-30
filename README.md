# apidays-example
Worked example from API Days (New York) Omnichannel workshop
Starting from a locally hosted instance of [privateGPT](https://github.com/zylon-ai/private-gpt), we will host and run [FreeClimb](https://www.freeclimb.com) application that provides the same experience via SMS, Voice, and (presuming available time) a simple web form.

This repository includes a [simple example constructed ahead of time](apidays/example.py) as well as the code that was created during the actual process of the demo. In addition a [script](setup.sh) that attempts to setup privateGPT for the demo is provided, without any guarantees as to accuracy or functionality.

## Steps to setup FreeClimb Application

1. Create FreeClimb Account <https://freeclimb.com/dashboard/login/>
2. Register a new FreeClimb Application ![screenshot showing how to register a FreeClimb Application](images/FC-Application.png)
3. Setup Voice Callback, SMS Callback, and Status Callback with server URL (ngrok or other means of exposing an application)
4. Purchase a FreeClimb phone number and assign to the FreeClimb Application created in step 2
5. Verify your server is receiving traffic when calling and texting the number

## FreeClimb Application Flow

```mermaid
sequenceDiagram
    participant fc as FreeClimb
    participant eu as End User
    participant s as Server
    eu ->> fc: Customer calls registered FreeClimb number
    fc ->> s: FreeClimb notifies server about incoming call
    s ->> s: Server determines expected action for call
    s ->> fc: Server returns response to FreeClimb request
    fc ->> eu: Accepts call, performs next PerCL action
    loop Previous PerCL Completed
    fc ->> s: FreeClimb returns result from PerCL, requests new PerCL
    s ->> fc: Server responds with new PerCL
    end
```

## Useful Links

- [FreeClimb Reference Documentation](https://docs.freeclimb.com/reference/api-reference-overview)
- [FreeClimb Python SDK](https://github.com/FreeClimbAPI/python-sdk)
- [FreeClimb Voice Quickstart](https://github.com/FreeClimbAPI/Python-Voice-Quickstart)
- [FreeClimb SMS Quickstart](https://github.com/FreeClimbAPI/Python-SMS-Quickstart)
- [privateGPT Installation](https://docs.privategpt.dev/installation/getting-started/main-concepts)
