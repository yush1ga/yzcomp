BODY = '''
function _{{name}}(){
  local context curcontext="$curcontext" state line
  typeset -A opt_args

  local ret=1
  local allowed_commands=({{ allowed_commands }})

  local cmd=''
  local option=''
  local cmd_pos=0
  local option_pos=0
  local pos=0

  for v in $(echo $LBUFFER); do
    if [[ $v =~ ^-.+ ]]; then
      option=$v
      option_pos=$pos
    else
      if [[ -n ${allowed_commands[(re)${v}]} ]]; then
        cmd+=_${v}
        cmd_pos=$pos
      fi
    fi
    (( pos++ ))
  done;
  
  if [ $cmd_pos -lt $option_pos ]; then
    local opt=${option#-}
    opt=${opt#-}
    cmd+=_${opt}
  fi

  case $cmd in
    {%- for case in cases %}
      {{- case}}
    {%- endfor %}
    (*)
      _arguments \
        '*: :_files -/' && ret=0 
  esac

  return $ret
}

{% for args in argss %}
{{ args }}
{% endfor %}
'''

CASE = '''
    ({{case}})
      _arguments \\
        {%- for opt in options %}
        {{opt}} \\
        {%- endfor %}
        '*: :{{args}}' && ret=0 
      ;;
'''

ARGS = '''
function {{ name }}() {
  local commands; commands=(
    {%- for arg in args %}
    '{{- arg }}'
    {%- endfor %}
  )
  _describe -t commands "{{name}}" commands "$@"
}
'''

VALUES = '''
function {{ name }}() {
  _values \\
    'values' \\
    {%- for value in values %}
    {{ value }} \\
    {%- endfor %}
}
'''