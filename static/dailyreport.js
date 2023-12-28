"use strict";

const $addCraft = $("#add-craft");
const $cancelCraft = $("#cancel-craft");
const $addCode = $("#add-code");
const $cancelCode = $("#cancel-code");

const $dailyReportForm = $("#daily-report-form");
const $addCraftForm = $("#craft-form");
const $addCodeForm = $("#cost-code-form");

const $craftRows = $("#craft-row tr")
const $craftRowContainer = $("#craft-row")

$addCraft.on("click", handleClickAddCraft);
$addCode.on("click", handleClickAddCode);

$cancelCraft.on("click", handleClickCancel);
$cancelCode.on("click", handleClickCancel);

$addCraftForm.on("submit", handleSubmitAddCraft);
// $addCodeForm.on("submit", handleSubmitAddCode);

/** handleClickAddCraft toggles the hidden property on the $addCraftForm*/
function handleClickAddCraft(evt) {
  $addCraftForm.toggleClass("hidden");
}

/** handleClickAddCode toggles the hidden property on the $addCodeForm*/
function handleClickAddCode(evt) {
  $addCodeForm.toggleClass("hidden");
}

/** handleClickCancel toggles the hidden property on the event target form*/
function handleClickCancel(evt) {
  const $target = $(evt.target.closest("form"));
  $target.toggleClass("hidden");
}

/** handleSubmitAddCraft toggles the hidden property on the event target and
 * adds the craft to the daily report form. */

function handleSubmitAddCraft(evt) {

  evt.preventDefault();
  const $target = $(evt.target.closest("form"));
  $target.toggleClass("hidden");

  const selectedCraftID = $("#craft-select").find(":selected").val();
  const selectedCraft = $("#craft-select").find(":selected").text();

  addCraft(selectedCraftID, selectedCraft);
}

/** addCraft takes in a craft ID and craft name, both strings.
 * -Add the craft name as a th element on a new tr element if craft isn't
 * already on the report
 * -Add new td cells into the row for every th element in the tr element in the
 * thead element
 */
function addCraft(id, name){
  console.log("addCraft", id, name);

  for(const $row of $craftRows) {
    if($row.data("craft") === id) return;
  }

  const $craftRow = $("<tr></tr>");
  const $craftHeader = $(
    `<th><button type="button" id="${id}" class="craft btn btn-success">${name}</button></th>`
  );

  $craftHeader.data("craft", `${id}`);

  $craftRow.append($craftHeader);

  const $codeCols = $("#code-col tr th");

  for(const $col of $codeCols) {
    const code = $col.data("code");
    $reportCell = $('<td><input type="number"></td>');
    $reportCell.data("craft", `${id}`)
    $reportCell.data("code", `${code}`)
    $craftRow.append($reportCell);
  }

  $craftRowContainer.append($craftRow);

}