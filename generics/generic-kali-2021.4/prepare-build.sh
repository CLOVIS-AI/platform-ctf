# $TF_VAR_generic_user and $TF_VAR_generic_password are strings
# shellcheck disable=SC2016
mkdir http
sed 's/$TF_VAR_generic_user/'"$TF_VAR_generic_user"'/ ; s/$TF_VAR_generic_password/'"$TF_VAR_generic_password"'/' preseed.tpl.cfg > http/preseed.cfg
