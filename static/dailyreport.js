"use strict";

const $addCraft = $("#add-craft");
const $cancelCraft = $("#cancel-craft");
const $addCode = $("#add-code");
const $cancelCode = $("#cancel-code");

const $dailyReportForm = $("#daily-report-form");
const $addCraftForm = $("#craft-form");
const $addCodeForm = $("#cost-code-form");

const $craftRowContainer = $("#craft-row")

$addCraft.on("click", showAddCraftForm);
$addCode.on("click", showAddCodeForm);

$cancelCraft.on("click", toggleHiddenClass);
$cancelCode.on("click", toggleHiddenClass);

$addCraftForm.on("submit", handleSubmitAddCraft);
$addCodeForm.on("submit", handleSubmitAddCode);

/** showAddCraftFrom toggles the hidden property on the $addCraftForm*/
function showAddCraftForm(evt) {
  $addCraftForm.toggleClass("hidden");
}

/** showAddCodeForm toggles the hidden property on the $addCodeForm*/
function showAddCodeForm(evt) {
  $addCodeForm.toggleClass("hidden");
}

/** showCraftNote toggles the hidden property on the craft note*/
function showCraftNote(evt) {

  const $button = $(evt.target)
  const $craftNotes = $("form div.craft-note")

  for(const note of $craftNotes) {
    if($(note).data("craft") === $button.data("craft")){
      $(note).toggleClass("hidden");
    }
  }
}

/** showCodeNote toggles the hidden property on the code note*/
function showCodeNote(evt) {

  const $button = $(evt.target)
  const $codeNotes = $("form div.craft-note")

  for(const note of $codeNotes) {
    if($(note).data("code") === $button.data("code")){
      $(note).toggleClass("hidden");
    }
  }
}

/** deleteResource will delete any resource added to the daily report. */
function deleteResource(evt) {
  console.log("deleteResource", evt)
  const resourceId = $(evt.target).attr("class");
  const $elements = $(`.${resourceId}`);

  for(const element of $elements) {
    $(element).remove();
  }

  const splitResourceId = resourceId.split("-");

  const $cells = $("td");

  for(const cell of $cells) {
    if($(cell).data(splitResourceId[0]) === splitResourceId[1]) {
      $(cell).remove();
    }
  }
}

/** toggleHiddenClass toggles the hidden property on the event target*/
function toggleHiddenClass(evt) {
  const $hiddenDiv = $($(evt.target).closest(".craft-note"));
  $hiddenDiv.toggleClass("hidden");
}

/** handleSubmitAddCraft toggles the hidden property on the event target and
 * adds the craft to the daily report form. */

function handleSubmitAddCraft(evt) {

  evt.preventDefault();
  const $target = $($(evt.target).closest("form"));
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
  const $craftRows = $("#craft-row tr")

  for(const row of $craftRows) {
    if($(row).data("craft") === id) return;
  }

  const $craftRow = $(`<tr class=craft-${id}></tr>`);
  const $craftHeader = $("<th></th>");

  const $craftHeaderButton = $(`
    <button
      type="button"
      class="craft btn btn-success btn-md">
        ${name}
    </button>`
  );

  $craftHeaderButton.data("craft", `${id}`);

  $craftHeaderButton.on("click", showCraftNote);

  $craftHeader.append($craftHeaderButton);

  const $craftHeaderSummary = $(`
    <div class="d-flex flex-column">
      <span>
        Total Mhrs:
        <span id="total-mhrs">
        </span>
      </span>
    </div>
  `)

  const $craftHeaderDeleteButton = $(`
    <button type="button" class="craft-${id}"><i class="bi bi-trash"></i></button>
  `)

  $craftHeaderDeleteButton.on("click", deleteResource);

  $craftHeaderSummary.append($craftHeaderDeleteButton);

  $craftHeader.append($craftHeaderSummary);

  const $craftNote = $(`
    <div class="
      popup
      hidden
      d-flex
      flex-column
      justify-content-around
      align-items-center
      craft-note
      craft-${id}">
      <label for="craft-notes-${id}">
        Notes
      </label>
      <textarea
        id="craft-notes-${id}"
        name="craft-notes-${id}"
        rows="8"
        cols="33"></textarea>
    </div>`
  );

  const $craftNoteButton = $(
    `<button
      type="button"
      class="btn btn-primary btn-md">
        Done
    </button>`
  );

  $craftNoteButton.on("click", toggleHiddenClass);

  $craftNote.append($craftNoteButton);

  $craftNote.data("craft", `${id}`);

  $dailyReportForm.append($craftNote);

  $craftHeader.data("craft", `${id}`);

  $craftRow.append($craftHeader);

  $craftRow.data("craft", `${id}`);

  const $codeCols = $("#code-col tr th");

  for(const col of $codeCols) {
    const code = $(col).data("code");
    if(code === undefined) continue;
    const $reportCell = $('<td><input type="number"></td>');
    $reportCell.data("craft", `${id}`);
    $reportCell.data("code", `${code}`);
    $craftRow.append($reportCell);
  }

  $craftRowContainer.append($craftRow);

}

/** handleSubmitAddCode toggles the hidden property on the event target and
 * adds the code to the daily report form. */

function handleSubmitAddCode(evt) {
  evt.preventDefault();
  const $target = $($(evt.target).closest("form"));
  $target.toggleClass("hidden");

  const selectedCode = $("#code-select").find(":selected").val();
  const selectedCodeName = $("#code-select").find(":selected").text();

  addCode(selectedCode, selectedCodeName);
}

/** addCode takes in a code and code name, both strings.
 * -Add the code name as a th element on a new tr element if code isn't
 * already on the report
 * -Add new td cells into each craft row that doesn't have a td cell already
 */
function addCode(code, name){
  const $codeCols = $("#code-col tr th");

  for(const col of $codeCols) {
    if($(col).data("code") === code) return;
  }

  const $codeHeader = $(`<th class="code-${code}"></th>`);

  const $codeHeaderButton = $(`
    <button
      type="button"
      class="code btn btn-success btn-md">
        ${name}
    </button>`
  );

  $codeHeaderButton.data("code", `${code}`);

  $codeHeaderButton.on("click", showCodeNote);

  $codeHeader.append($codeHeaderButton);

  const $codeHeaderSummary = $(`
    <div class="d-flex flex-column">
      <span>
        Total Mhr:
        <span id="total-mhrs">
        Total Qty:
        <span id="total-qty">
        </span>
      </span>
    </div>
  `)

  const $codeHeaderDeleteButton = $(`
    <button type="button" class="code-${code}"><i class="bi bi-trash"></i></button>
  `)

  $codeHeaderDeleteButton.on("click", deleteResource);

  $codeHeaderSummary.append($codeHeaderDeleteButton);

  $codeHeader.append($codeHeaderSummary);

  const $codeNote = $(`
    <div class="
      popup
      hidden
      d-flex
      flex-column
      justify-content-around
      align-items-center
      craft-note
      code-${code}">
      <label for="code-notes-${code}">
        Notes
      </label>
      <textarea
        id="code-notes-${code}"
        name="code-notes-${code}"
        rows="8"
        cols="33"></textarea>
    </div>`
  );

  const $codeNoteButton = $(
    `<button
      type="button"
      class="btn btn-primary btn-md">
        Done
    </button>`
  );

  $codeNoteButton.on("click", toggleHiddenClass);

  $codeNote.append($codeNoteButton);

  $codeNote.data("code", `${code}`);

  $dailyReportForm.append($codeNote);

  $codeHeader.data("code", `${code}`);

  const $codeRow = $("#code-col tr");

  $codeRow.append($codeHeader);

  const $craftRows = $("#craft-row tr")

  for(const row of $craftRows) {
    const id = $(row).data("craft");
    const $reportCell = $('<td><input type="number"></td>');
    $reportCell.data("craft", `${id}`);
    $reportCell.data("code", `${code}`);
    $(row).append($reportCell);
  }

}