# Création du modèle pour ce scénario

**Utilise :** `generic_windows_10_enterprise` la VM générique Windows 10
              `generic_windows_server_2019` la VM générique Windows server 2019
              `generic_kali_2020.4` la VM générique Kali version 2020.4
              `generic_pfsense` la VM générique PfSense


Exécuter ces commandes (en remplaçant bien l'utilisateur et le password par les bonnes valeurs) : 

```
terraform plan --out plan.out -var 'vcenter_host=172.21.253.252' -var 'vcenter_user=<utilisateur>' -var 'vcenter_password=<password>'
terraform apply plan.out
```

Il faut maintenant configurer le pfsense grâce à la configuration `config_pfsense.xml`

Il s'agit ensuite d'éxécuter les différents scripts Ansible :
    - Vérifier la présence de la bonne configuration des hosts ansible, un modèle est présent dans le dossier `ansible` (vérifier le dossier group_vars).
    - Vérifier la présence de la variable de configuration `host_key_checking = false` au sein du fichier `/etc/ansible/ansible.cfg`
    - Dans le dossier Ansible :

    ```
    ansible-playbook kali.yml
    ansible-playbook 1_windowsServer.yml
    ansible-playbook 2_windows10.yml
    ansible-playbook 3_windowsServer.yml
    ```

Il suffit maintenant d'éteindre la VM et de faire une snapshot. Le modèle est maintenant utilisable par le fichier Terraform de ce challenge. 
