# Binary Art Generator

This project converts images into binary art. The script takes an input image and generates a text file containing the binary art representation of the image.

## Usage

### Arguments
- `-i, --image_path` : Path to the input image file.
- `-o, --output_file` : Path to the output text file where binary art will be saved.
- `-w, --width` : Optional. Width of the output binary art. Default is 100.
- `-b, --bg_adjust` : Optional. Background adjustment type: 'bright', 'dark', or 'none'. Default is 'none'.
- `-t, --tolerance` : Optional. Tolerance for background color removal. Default is 30.

## Examples

### Convert an image to binary art with default settings:
`python binary_art.py -i input.jpg -o output.txt`

### Convert an image to binary art with a specified width:
`python binary_art.py -i input.png -o output.txt -w 80`

### Convert an image to binary art with background adjustment:
`python binary_art.py -i input.jpeg -o output.txt -b bright`

## Example Binary Art
```                                                                                           
                                                 01110                                              
                                             01111111110                                            
                                         00111111111111110                                          
                                      011111111101110111110                                         
                                  01111111111    1011 1111110                                       
                              01111111111111110    000011111110                                     
                           111111111111111111111    1111111111110                                   
                          11111111111111111111111111111111111111110                                 
                         0111111110   1111111111111111111111111111110                               
                        01 01111   0   1111111111111111111111000111111                              
                        1110 1111    01111111111111111110       111111100                           
                       011111  1111111111111111111111         011111111111                          
                       11111111 01111111111111111111111   011111111111110 1                          
                       111111111  11111111111111111111111111111111111111 11                        
                       01111111111  1111110 0111111111111111111111111111100                     
                         11111111110 0111111  11111111111111111111111111100                    
                          01111111111  111111  1111111111111111111111111100                  
                           111111111111  1111111111111111111111111111111100                    
                             11111111111  111111111111111111111111111111110                        
                              00111111111 0111111111111111111111111111110                           
                                011111111  111111111111111111111111110                              
                                 01111111 0111111111111111111111110                                 
                                   111111 0111111111111111111111                                    
                                     1111 1111111111111111111                                       
                                      111 1111111111111110                                          
                                       00 111111111110                                              
                                           11111110                                                 
                                           00110                                                    
```
--- 
> Enjoy creating your own binary art!