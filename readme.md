# ASCII Art Generator

This project converts images into ASCII art. The script takes an input image and generates a text file containing the ASCII art representation of the image.

## Usage

### Arguments
- `-i, --image_path` : Path to the input image file.
- `-o, --output_file` : Path to the output text file where ASCII art will be saved.
- `-w, --width` : Optional. Width of the output ASCII art. Default is 100.
- `-b, --bg_adjust` : Optional. Background adjustment type: 'bright', 'dark', or 'none'. Default is 'none'.
- `-t, --tolerance` : Optional. Tolerance for background color removal. Default is 30.

## Examples

### Convert an image to ASCII art with default settings:
`python ascii_art.py -i input.jpg -o output.txt`


### Convert an image to ASCII art with a specified width:
`python ascii_art.py -i input.jpg -o output.txt -w 80`

### Convert an image to ASCII art with background adjustment:
`python ascii_art.py -i input.jpg -o output.txt -b bright`

## Example ASCII Art
```

                                                             +***+                                              
                                                         +**#%%%%#*+                                            
                                                     ++*##%%@%%%%%%#*+                                          
                                                  +**#%%@%%#+#**+*%%%#+                                         
                                             ++**#%%@@%%*    *+** *#%%%*+                                       
                                         ++**#%%%@%%%%%%##+    ++++#%%%@%*+                                     
                                       **#%%%%%@%%%%%%%%%%#*    *#%%%%%%@@%*+                                   
                                      %%%@%#%%%#%@@%%%%%%%%%##%%%%%%%%%@@@@@%*+                                 
                                     +*%@@%#%#+   #%%%%%%%%%%%%%%%%%@@@@@@@@@@%*+                               
                                    +* +#%@#   +   #@%%%%%%%%%%%%@%%%****+++#@@@%*                              
                                    ###+ *%%#    +#%%%%%%%%%%%%%##**+       %@@@@@#++                           
                                   +##%%#  #%@%%%@@%%%%%%%%%%%%%*         +%@@@%%###**                          
                                   ##%%%%#* +#@@@@@@@@@%%%%%%%%%%%*   +%##@%%###%%@# *                          
                                   %%%%%%%%#  *%@@@%**#%@@%%%%%%%%@%**%@%%####%@@@@%  *                         
                                   +##%%%%%%#*  #@@%#*+ +#@%%@@%%@@@%%####%%@@@@@@@@*++++                      
                                     *##%%%%%%#+ +%@@@@#  #@@@@@%%%####%%@@@@@@@@@@@% +++++                    
                                      +##%%%%###*  *%@@@%  @@%%####%%@@@@@@@@@@@@@@@@*++++++                   
                                        *#%%%%####*  #%@%##%###%%@@@@@@@@@@@@@@@@@@%%*+++++                    
                                         *%%%%###%#  *%%###%%@@@@@@@@@@@@@@@@@@@%%##**+                        
                                           +#%#####%# +%@@@@@@@@@@@@@@@@@@@@@%%%%##*+                           
                                            #%%%####  @@@@@@@@@@@@@@@@@%%#*###**+                              
                                             +#%%%%%# +@@@@@@@@@@@@@@%##*##%#*+                                 
                                               *#%%%# +@@@@@@@@@@@@%###%%%#*                                    
                                                 #%%# *@@@@@@@@@@%%##%%#*                                       
                                                  *%# *@@@@@@@%%%##**+                                          
                                                   ++ #@@@@%%##**+                                              
                                                       #####**+                                                 
                                                       ++**+ 
```
---
> Enjoy creating your own ASCII art!