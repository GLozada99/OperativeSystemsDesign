#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <ctype.h>
#include <limits.h>

int main(int narg, char* argv[]){
    
    if(narg>=3){
        FILE *start, *end;
        size_t size_read = 1, size_write = 1;
        char *buffer, *overwr;
        char *source, *dest;
        int arguments = 3;
        char choise='N';
        int overwrite = 1;

        overwr = argv[1];
        
        if(strcmp(overwr,"-i")==0){ 
            arguments = 4;
            source = argv[2];
            dest = argv[3];
        }else{
            source = argv[1];
            dest = argv[2];
        }
        
        if(narg==arguments){
            if(arguments==4){
                if(access(dest,F_OK)==0){
                    printf("The destination File already exists. Would you like to overwrite? (Y/N) ");
                    fflush(stdin);
                    scanf(" %c", &choise);
                    choise = toupper(choise);
                    while(choise!='Y' && choise!='N'){
                    
                    printf("Answer with Y or N ");
                    
                    fflush(stdin);
                    scanf(" %c", &choise);
                    choise = toupper(choise);
                    }
                    if(choise=='N'){
                        overwrite = 0;
                        printf("Copy aborted\n");
                        return 0;
                    }
                }
            }else{
                if(access(dest,F_OK)==0){
                    overwrite = 0;
                    printf("Destination File already exists. Copy aborted\n");
                    return 0;
                } 
            }
            if(overwrite==1){
                start = fopen(source,"rb");
                end = fopen(dest,"wb");

                if(start!=NULL){
                    while((size_write == size_read) && size_read){
                        size_read = fread(buffer,1,sizeof(buffer),start);
                        if(size_read!=0){
                            size_write = fwrite(buffer,1,size_read,end);
                            
                        }else{
                            size_write = 0;
                        }
                    }
                    printf("File copy was succesful\n\n");
                }else{
                    printf("File %s doesn't exist\n\n",source);
                }

            fclose(start);
            fclose(end);
            }

        }else{
            printf("Must input only source and destination file\n\n");
        }
    }else{
        printf("To few arguments input\n");
    }

    return 0;
}
