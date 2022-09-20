const slideValue = document.querySelector("span");
const inputSlider = document.querySelector("input");
inputSlider.oninput = (() => {
  let value = inputSlider.value;
  slideValue.textContent = value;
  slideValue.style.left = (value) + "%";
  slideValue.classList.add("show");
});
inputSlider.onblur = (() => {
  slideValue.classList.remove("show");
});

function random(){
  const hline = document.createElement("hr");
  hline.className ="line";
  document.body.appendChild(hline);

  const form = document.createElement("form");
  
  const label1 = document.createElement("label")
  label1.for = "numbodies";
  label1.innerHTML="Number of bodies";
  const text = document.createElement("input")
  text.type = "range";
  text.id = "numbodies";
  text.min = "2";
  text.max = "100";
  text.step = "1";
  text.value = "5";
  //text.setAttribute(la) = "Number of bodies"
  form.appendChild(label1)
  form.appendChild(text)
  const label2 = document.createElement("label")
  label2.className="switch";
  const input2 = document.createElement("input")
  input2.type = "checkbox";
  const span2 = document.createElement("span")
  span2.class = "slider";
  label2.appendChild(input2)
  label2.appendChild(span2)
  form.appendChild(label2)

  document.body.appendChild(form);
}