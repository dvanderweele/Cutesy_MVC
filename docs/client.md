The `Client` system is how the View/UI layer will interact with the rest of the application (i.e. the controllers, models, and database).

The `Client` class is intended to be instantiated once for each UI component that will generate requests for your controllers. The client class has a single server thread held and managed in class attributes. Each client object may interact with the server thread through its methods. 

*To be clear, each individual `Client` object does NOT get its own server thread.*

It is required to pass a reference to a callback function into the `Client` constructor. When a response is pulled out of the response queue later, that method will have the response object passed into it as an argument. 

When you instantiate a client object, it is assigned a `uuid` on its `id` attribute. A class attribute keeps track of all active `Client` objects via those `uuid`s. The `uuid` is automatically attached to the `requester` key in the `header` sub-dictionary of request dictionaries generated with a `Client`'s `freshRequest` method (which can optionally take an argument specifying the 'route' value to store in the 'header' sub-dictionary of the request). 

Sending a request to the server thread is as simple as using the `send` method each `Client` provides. Of course, pass in your request dictionary as an argument.  Additional information your controllers need to fulfill a request (i.e. besides the route) should be attached to the 'payload' attribute of the request dictionary.

Probably at least once every time through your main application loop you will want to check if there are any responses in the response queue by using the `receive` method available on any `Client` object. It may be helpful to have a single top-level client in your application that is responsible both for periodically polling the response queue as well as calling `shutdown` to wnd the server thread when it is time to close your application.