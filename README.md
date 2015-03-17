# Trichome
A simple tool to fuzz test a web-based application.
> Here you stand, a Gladiator, in the Coliseum of Testing.

### Usage

````shell 
python3 trichome.py [discover | test] url OPTIONS`
````

#### Commands
```` 
trichome discover
````
prints a comprehensive list of all discovered inputs to the system. Techniques include crawling + guessing. 

```` 
trichome test
````
discovers all inputs, then attempts a list of exploit vectors on these inputs.

#### Flags
````
--custom-auth=string
````
tells Trichome to use hard-coded auth for a specific application (e.g. dvwa).  

````
--common-words=file
````
newline-delimited file of common words to be used in page guessing and input guessing.  

````
--vectors=file
````
newline-delimited file of common exploits to vulnerabilities.  

````
--sensitive=file
````
newline-delimited file data that should never be leaked. It's assumed that this data is in the application's database (e.g. test data), but is not reported in any response.   

````
--random
````
Choose a random page, then a random input field and test all vectors. Default: false.  

````
--slow=500
````
number of milliseconds considered when a response is considered "slow". Default: 500 milliseconds  

### Examples:
##### Discover inputs:  
````shell
python3 trichome.py discover http://localhost:8080 --common-words=mywords.txt
````  

##### Discover inputs to DVWA using hard-coded authentication:  
````
python3 trichome.py discover http://localhost:8080 --common-words=mywords.txt
````  

##### Discover and Test DVWA without randomness:  
````
python3 tricome.py test http://localhost:8080 --custom-auth=dvwa --common-words=words.txt --vectors=vectors.txt --sensitive=creditcards.txt --random=false
````

### Wiki
[Check out our wiki for how to use Trichome](https://github.com/piperchester/trichome/wiki)
