#!/bin/sh
PRODUCTNAME='ContentLicensing'
I18NDOMAIN=$PRODUCTNAME


i18ndude=$INS/bin/i18ndude

[[ ! -f $i18ndude ]] && i18ndude=i18ndude
echo using $i18ndude

# Synchronise the .pot with the templates.
$i18ndude rebuild-pot --pot ./locales/${PRODUCTNAME}.pot  --create ${I18NDOMAIN} ./
$i18ndude rebuild-pot --pot ./i18n/plone.pot --create plone ./profiles || exit 1

# Synchronise the resulting .pot with the .po files
$i18ndude sync --pot ./locales/${PRODUCTNAME}.pot ./locales/*/LC_MESSAGES/${PRODUCTNAME}.po
$i18ndude sync --pot ./i18n/plone.pot ./i18n/plone-*.po

WARNINGS=`find ./ -name "*pt" | xargs i18ndude find-untranslated | grep -e '^-WARN' | wc -l`
ERRORS=`find ./ -name "*pt" | xargs i18ndude find-untranslated | grep -e '^-ERROR' | wc -l`
FATAL=`find ./ -name "*pt"  | xargs i18ndude find-untranslated | grep -e '^-FATAL' | wc -l`

echo
echo "There are $ERRORS errors \(almost definitely missing i18n markup\)"
echo "There are $WARNINGS warnings \(possibly missing i18n markup\)"
echo "There are $FATAL fatal errors \(template could not be parsed, eg. if it\'s not html\)"
echo "For more details, run \'find . -name \"\*pt\" \| xargs i18ndude find-untranslated\' or" 
echo "Look the rebuild i18n log generate for this script called \'rebuild_i18n.log\' on locales dir" 

touch ./rebuild_i18n.log

find ./ -name "*pt" | xargs $i18ndude find-untranslated > ./locales/rebuild_i18n.log
