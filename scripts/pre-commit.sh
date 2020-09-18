isort . #  --verbose
black . #  --verbose

#

themes_names=(
    'sorolla'
    # 'sargent'
)

# https://blog.mimacom.com/arrays-on-linux-shell/
for theme_name in ${themes_names[@]}; do

    theme_root="./src/easel/themes/$theme_name"

    prettier="$theme_root/node_modules/prettier/bin-prettier.js"
    gulp="$theme_root/node_modules/gulp/bin/gulp.js"

    $prettier \
        "$theme_root/assets/scss/**/*.scss" \
        "$theme_root/assets/typescript/**/*.ts" \
        --config "$theme_root/.prettierrc" \
        --write

    $gulp \
        --gulpfile "$theme_root/gulpfile.js" \
        --cwd "$theme_root" \
        build
done