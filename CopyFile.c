#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <ctype.h>
#include <limits.h>

int check(int arguments,char *source, char *dest);
void copy_file(char *source, char *dest);

int main(int narg, char* argv[]){
    if(narg>=3){
        char *source, *dest;
        int arguments = 3;

        if(strcmp(argv[1],"-i")==0){ 
            arguments = 4;
            source = argv[2];
            dest = argv[3];
        }else{
            source = argv[1];
            dest = argv[2];
        }

        if(realpath(dest,NULL)!=NULL)
            dest = realpath(dest,NULL);

        if(realpath(source,NULL)!=NULL)
            source = realpath(source,NULL);    
            
        printf("%s\n\n",source);
        printf("%s\n\n",dest);
        if(strcmp(source,dest)!=0){
            if(narg==arguments){
                if(check(arguments,source, dest)==1){
                    copy_file(source,dest);
                }    
            }else{
                printf("Must input only source and destination file\n");
            }
        }else{
            printf("Source and Destination files are the same\n");
        }
    }else{
        printf("To few arguments input\n");
    }
    return 0;
}
int check(int arguments, char *source, char *dest){//Checks whether the file should be copied or not 
    char choise = 'N';
    if(access(source,F_OK)!=0){
        printf("Source File does not exists. Copy aborted\n");
        exit(0);
    } 
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
                printf("Copy aborted\n");
                exit(0);
            }
        }
    }else{
        if(access(dest,F_OK)==0){
            printf("Destination File already exists. Copy aborted\n");
            exit(0);
        } 
    }
    return 1;

}

void copy_file(char *source, char *dest){//Copies the file from the source to the destination address
    FILE *start, *end;
    size_t size_read = 1, size_write = 1;
    char buffer[4096];

    start = fopen(source,"rb");
    end = fopen(dest,"wb");

    if(start!=NULL && end!=NULL){
        while((size_write == size_read) && size_read){
            size_read = fread(buffer,1,sizeof(buffer),start);
            if(size_read!=0){
                size_write = fwrite(buffer,1,size_read,end);
                
            }else{
                size_write = 0;
            }
        }
        printf("File copy was succesful\n");
    }else{
        printf("Error opening files");
    }

    fclose(start);
    fclose(end);
}
