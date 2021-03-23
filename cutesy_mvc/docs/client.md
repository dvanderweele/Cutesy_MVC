The `Client` system is how the View/UI layer will interact with the rest of the application (i.e. the controllers, models, and database).

The `Client` class is intended to be instantiated once for each UI component that will generate requests for your controllers. The client class has a single server thread held and managed in class attributes. Each client object may interact with the server thread through its methods. 

*To be clear, each individual `Client` object does NOT get its own server thread.*

When you instantiate a client object, it is assigned a `uuid` on its `id` attribute. A class attribute keeps track of all active `Client` objects through a list pf those `uuid`s. The `uuid` is automatically attached to the `requester` key in the `header` sub-dictionary of request dictionaries generated with a `Client`'s `freshRequest` method (which can optionally take an argument specifying the 'route' value in to store in the 'header' sub-dictionary of the request). 

Sending a request to the server thread is as simple as using the `send` method each `Client` provides. Of course, pass in your request dictionary as an argument.  Additional information your controllers need to fulfill a request (i.e. besides the route) should be attached to the 'payload' attribute of the request dictionary.

Probably at least once every time through your main application loop you will want to check if there are any responses in the response queue by using the `receive` method available on any `Client` object. If there is a response dictionary, check it for the `uuid` that generated its request. With that `uuid` in hand, use the `valid` method `Client` provides to make sure the UI component that generated the request still exists. If it does, use whatever algorithm is appropriate to you to deliver that response to the appropriate part of the UI.