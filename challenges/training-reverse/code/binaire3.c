#include <stdio.h>
#include <string.h>

int criteria(char* c){
    int n=strlen(c);
    char my_code[9];
    strcpy(my_code, "goodluck");
    * my_code = 57;
    if ((n == 8) && (* c == 52) && (c[2] == (int)my_code[1] + (int)my_code[0] - (int)my_code[6]) && (c[1]== 'o') && (c[9-3] == 'l') && (c['F'%13] == '@') && (c[3]== c[7]) && (c[80-19*4] == 'k')){
        return 1;
    }
    return 0;
  }

int main (int argc, char* argv[]){
  if (argc <=1){
      printf("Il faut mettre au moins un paramètre! Je vais pas juste te donner le mot de passe non plus!\n");
      return 1;
  }
  if (argc > 2){
      printf("Ca sert à rien de mettre plus d'une tentative. Je testerai que la première ;-)\n");
  }
  char p=* (argv[1] + 3*sizeof(char));
  int result = criteria(argv[1]);
  if ((result) && (p == 'W')){
      printf("bien joué, vous avez trouvé le flag\n");
  }
  else {
      printf("bien tenté mais non \n");
  }
  return 0;
}
