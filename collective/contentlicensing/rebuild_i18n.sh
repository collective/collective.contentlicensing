#!/bin/sh
PRODUCTNAME='ContentLicensing'
I18NDOMAIN=$PRODUCTNAME


i18ndude=$INS/bin/i18ndude

[[ ! -f $i18ndude ]] && i18ndude=i18ndude
echo using $i18ndude

# Synchronise the .pot with the templates.
$i18ndude rebuild-pot --pot locales/${PRODUCTNAME}.pot  --create ${I18NDOMAIN} .

# Synchronise the resulting .pot with the .po files
$i18ndude sync --pot locales/${PRODUCTNAME}.pot locales/*/LC_MESSAGES/${PRODUCTNAME}.po


