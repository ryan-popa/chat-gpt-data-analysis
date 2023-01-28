# Chat GPT for data visualisation

This tool takes an instruction in text format and generates the code to create pyplot charts.

example imput: `given the titanic dataset display a correlation matrix for the survivors based on the fare paid for the ticket`.

ChatGPT is awesome at generating code but future fine tuning will be needed.
However it will be able to generate useful code that can act as the starting point which can be copied into a jupyter notebook.

# Security 
It uses an unsafe way of running python code so best to just run this locally or in a safe environment. Unfortunatelly creating a [safe sandbox environment for Python execution is non trivial](https://stackoverflow.com/questions/3068139/how-can-i-sandbox-python-in-pure-python). Instead of trying to create the sandbox environment inside the application it might work best to do it at the infrastructure level by spinning off worker nodes that execute the unsafe code (using Kubernetes for example).

# Set up
```
echo "OPENAI_API_KEY=your_api_key" > secrets.env
make build # only needed the first time
make run
```
