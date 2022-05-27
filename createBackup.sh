
declare -r GC='\033[1;32m' # green color
declare -r YC='\033[1;33m' # yellow color
declare -r RC='\033[1;31m' # red color
declare -r NC='\033[0m'    # no color
declare src_file="$1"
declare des_file="$2"
declare project_name=$(basename $src_file)
declare -a backup_list
declare keptBackup=5
declare agent_user="mahfakhr"

if [ -z $agent_user ]; then
    echo 'agent user is empty'
    agent_user='mahfakhr'
fi

function info_echo {
    declare -r log_date=$(date +'%Y-%m-%d %H:%M:%S')
    echo -e "${YC}[ INFO ] [ $log_date ] [$1] $2 ${NC}"
}

function error_echo {
    declare -r log_date=$(date +'%Y-%m-%d %H:%M:%S')
    echo -e "${RC}[ ERROR ] [ $log_date ] [$1] $2${NC}"
}

function success_echo {
    declare -r log_date=$(date +'%Y-%m-%d %H:%M:%S')
    echo -e "${GC}[ SUCCESSFUL ] [ $log_date ] [$1] $2${NC}"
}
if [ $# -lt 2 ]; then
    echo 'stop bash args are not sufficient'
    exit
fi

function sort_array {
    # input:
    #       @ an array
    if [ -n "$1" ]; then
        local IFS=$'\n'
        eval "local arr=( \${$1[*]} )"
        arr=($(sort --reverse <<<"${arr[*]}"))
        eval "$1=( \${arr[*]} )"
    fi
}

des_file="$des_file/$(basename $src_file)"
if [ -e $src_file ]; then
    if [ -e $des_file ]; then
        [ -f $des_file ] && return 2
    else
        sudo -u $agent_user mkdir -p "$des_file"
        success_echo "Create backup" "destination directory created successfully!"
    fi
    while true; do
        if [ ! -e "${des_file}/$(date +"%Y%m%d%H%M%S")" ]; then
            sudo -u $agent_user cp -r "$src_file" "${des_file}/$(date +"%Y%m%d%H%M%S")"
            if [ $? -eq 0 ]; then
                success_echo "Create backup" "done copy file $src_file"
            else
                error_echo "Create backup" "error in creating file"
                exit 1;
            fi
            break
        fi
    done
    
    backup_list=("${des_file}"/*)
    sort_array backup_list
    sudo -u $agent_user rm -rf "${backup_list[@]:$keptBackup}"
else
    error_echo  "Create backup" "source directory is not available"
fi