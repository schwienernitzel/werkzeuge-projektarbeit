#!/bin/bash
if [[ -z "${INPUT_FILE}" ]]; then
  echo "ERROR: Umgebungsvariable INPUT_FILE ist nicht gesetzt."
  exit 1
fi

if [[ -z "${REMOVE}" ]]; then
  echo "ERROR: Umgebungsvariable REMOVE ist nicht gesetzt."
  exit 1
fi

input_file="${INPUT_FILE:-input.csv}"
touch hate-clean.csv
output_file="hate-clean.csv"
word_to_remove="${REMOVE}"

if [[ ! -f "$input_file" ]]; then
  echo "Eingabedatei '$input_file' nicht gefunden!"
  exit 1
fi

num_lines_before=$(wc -l < "$input_file")
grep -v "$word_to_remove" "$input_file" > "$output_file"
num_lines_after=$(wc -l < "$output_file")

if [[ $? -eq 0 ]]; then
  echo "Die Datei wurde erfolgreich bereinigt. Es sind $num_lines_after Zeilen übrig geblieben (vorher: $num_lines_before)."
else
  echo "Fehler beim Bereinigen der Datei."
  exit 1
fi

mv $output_file out/