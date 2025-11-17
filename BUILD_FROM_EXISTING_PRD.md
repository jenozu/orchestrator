# Building an App from Existing PRD and MVP Files

## 🎯 Workflow Overview

If you already have PRD and MVP markdown files, here's the step-by-step process:

1. **Parse your PRD/MVP** → Get structured requirements
2. **Generate the project** → Build the actual codebase
3. **(Optional) Search for patterns** → Find similar code examples first

---

## 📝 Step-by-Step Prompts

### Step 1: Parse Your PRD/MVP Files

**If you have a PRD file:**
```
Use parse_prd to parse my PRD file at docs/prd.md and convert it into structured requirements
```

**If you have an MVP file:**
```
Use parse_prd to parse my MVP document at docs/mvp.md into structured JSON requirements
```

**If you have both:**
```
First, use parse_prd to parse docs/prd.md into structured requirements. Then also parse docs/mvp.md and combine the requirements.
```

**Alternative phrasing:**
- "Parse docs/prd.md using parse_prd to extract structured requirements"
- "Convert my PRD at docs/prd.md to JSON format using parse_prd"
- "Use parse_prd on docs/mvp.md to get structured requirements"

---

### Step 2: Generate the Project

**After parsing, generate the codebase:**

```
Use generate_project to build the complete app from the parsed requirements. Save it to the "generated_app" directory.
```

**If you want to specify the output location:**
```
Use generate_project to generate the project from the requirements we just parsed, and output it to "my_app" directory
```

**More specific:**
```
Use generate_project with the requirements from the parsed PRD to generate the full project structure in the "app" folder
```

---

## 🚀 Complete Workflow (One Conversation)

You can do this all in one go:

```
I have a PRD at docs/prd.md and an MVP at docs/mvp.md. 

First, use parse_prd to parse docs/prd.md into structured requirements. 
Then use parse_prd to also parse docs/mvp.md and merge those requirements.

Finally, use generate_project to build the complete application from these combined requirements, outputting to the "app" directory.
```

**Or more naturally:**
```
I have my PRD and MVP written up in docs/prd.md and docs/mvp.md. 

Please:
1. Parse both documents using parse_prd to get structured requirements
2. Use generate_project to build out the complete app in the "app" folder based on those requirements
```

---

## 🔍 Optional: Search for Patterns First

Before generating, you might want to find similar code patterns:

```
Before generating, use retrieve_context to find FastAPI authentication patterns and React component examples that match my PRD requirements
```

**Then:**
```
Now use generate_project to build the app, incorporating the patterns we found
```

---

## 📋 Example Full Conversation

**You:**
```
I have my PRD at docs/my_project_prd.md and MVP at docs/mvp.md. I want to build out the full application. 

First, parse both documents using parse_prd to get structured requirements. Then use generate_project to create the complete codebase in the "my_app" directory.
```

**Cursor will:**
1. Parse `docs/my_project_prd.md` → Get structured requirements
2. Parse `docs/mvp.md` → Get additional requirements
3. Generate the complete project in `my_app/` directory

---

## 🎯 Specific Use Cases

### If Your PRD is in a Different Location

```
Use parse_prd to parse the PRD at C:\Users\andel\Desktop\my_project\requirements.md
```

### If You Want to Generate to a Specific Path

```
Use generate_project to build the app from the parsed requirements and save it to "C:\Users\andel\Desktop\generated_app"
```

### If You Want to Include RAG Context

```
First, use retrieve_context to find similar projects and patterns for [your tech stack, e.g., "React + FastAPI + PostgreSQL"]. 

Then use parse_prd to parse docs/prd.md, and finally use generate_project to build the app incorporating those patterns.
```

---

## 💡 Pro Tips

1. **Be Specific About File Paths**: 
   - ✅ "Parse docs/prd.md"
   - ❌ "Parse my PRD" (too vague)

2. **Specify Output Directory**:
   - ✅ "Generate to 'app' directory"
   - ❌ "Generate the project" (might use default location)

3. **Combine Both Documents**:
   - If you have both PRD and MVP, parse both and mention you want them combined

4. **Use RAG for Better Results**:
   - Search for patterns first, then generate - the generator will use those patterns

5. **Check Generated Files**:
   - After generation, review the output directory structure

---

## 🔄 Alternative: Direct Generation

If you want to skip the parsing step and go straight to generation (though parsing is recommended):

```
Use generate_project to build an app based on the requirements in docs/prd.md. Output to "app" directory.
```

However, **parsing first is better** because:
- It converts your markdown into structured JSON
- The generator works better with structured requirements
- You can review/modify the requirements before generation

---

## 📁 Expected Output

After running `generate_project`, you should see:
- Complete project structure
- All source files
- Configuration files
- README and documentation
- Dependencies list

All in the output directory you specified!

---

## 🛠️ Troubleshooting

### "File not found" error
- Make sure the file path is correct
- Use relative paths from project root (e.g., `docs/prd.md`)
- Or use absolute paths (e.g., `C:\Users\andel\Desktop\orchestrator\docs\prd.md`)

### "Requirements not structured" error
- Make sure you parsed the PRD first using `parse_prd`
- The generator needs structured JSON, not raw markdown

### Generated code doesn't match PRD
- Try parsing again with more specific instructions
- Use `retrieve_context` to find better patterns first
- Review the parsed requirements before generating

---

## 🎉 Quick Start Command

**Copy and paste this (adjust file paths):**

```
I have my PRD at docs/prd.md. Please:
1. Use parse_prd to parse it into structured requirements
2. Use generate_project to build the complete app in the "app" directory
```

That's it! The tools will handle the rest. 🚀

