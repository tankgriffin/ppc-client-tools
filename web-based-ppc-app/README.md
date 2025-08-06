# PPC Strategic Intelligence Web App

A comprehensive web application for conducting strategic PPC campaign research using Claude AI's 5-phase methodology.

## Features

### Project Management
- **Dashboard**: Overview of all projects with status tracking and search/filter capabilities
- **Project Creation**: Multi-step wizard to collect comprehensive business intelligence
- **Project Workspace**: Dedicated space for each research project with phase management
- **Analysis Dashboard**: Comprehensive analysis view with graphs, insights, and export capabilities
- **Auto-Status Updates**: Projects automatically progress from draft to completed when all phases are done

### Claude AI Research Integration
- **Service Package Support**: Choose between PPC Only, SEO Only, or PPC + SEO Combined packages
- **5-Phase Research Framework** (tailored to your service package):
  1. **Business Intelligence Analysis** - Market position and competitive advantages
  2. **Competitive Landscape Mapping** - Direct and indirect competitor analysis
  3. **Market Gap Identification** - Untapped opportunities and positioning gaps
  4. **Strategic Positioning Development** - Differentiation and messaging strategy
  5. **Content & Campaign Strategy** - Implementation roadmap and tactical execution

### Smart Prompt Generation
- **Service-Package Aware**: Prompts automatically adapt based on PPC, SEO, or combined service selection
- **Dynamic Prompts**: Automatically generates comprehensive, context-aware prompts for Claude AI
- **Business Context Integration**: All prompts include relevant business details and objectives
- **Copy-to-Clipboard**: Easy workflow for using prompts with Claude AI
- **Response Management**: Save and organize Claude AI responses within the application

### Analysis & Insights
- **Executive Dashboard**: Visual overview of opportunities, risks, and recommendations
- **Interactive Tabs**: Navigate between overview, opportunities, strategy, timeline, metrics, and research data
- **Intelligent Extraction**: Automatically extracts key insights from Claude AI responses
- **Strategic Roadmap**: 4-phase implementation timeline with actionable milestones
- **Success Metrics**: Customized KPI tracking based on business goals
- **Export Reports**: Download comprehensive analysis reports in text format

### Implementation Planning
- **12-Month Roadmap**: Detailed month-by-month implementation planning system
- **Automated Task Extraction**: AI-powered extraction of actionable tasks from Claude responses
- **Task Management**: Complete task tracking with categories, priorities, time estimates, and assignments
- **Progress Tracking**: Visual progress indicators and completion rates for each month
- **Budget Allocation**: Monthly budget distribution based on selected budget range
- **Service-Package Optimization**: Tasks and goals tailored to PPC, SEO, or combined strategies
- **Interactive Planning**: Add, edit, delete, and complete tasks with full project management capabilities

### Data Management
- **Local Storage**: All data stored locally in browser using IndexedDB
- **Auto-Save**: Automatic saving of project progress and responses
- **Smart Status Tracking**: Projects automatically progress through draft, in-progress, and completed states
- **Project Templates**: Reusable templates for common industry types

## Technology Stack

- **Frontend**: Next.js 14 with App Router, TypeScript, Tailwind CSS
- **Icons**: Lucide React icon library
- **Storage**: Browser localStorage with structured data management
- **UI Components**: Custom component library with consistent design system

## Getting Started

### Prerequisites
- Node.js 18+ and npm
- Modern web browser with localStorage support

### Installation

1. Clone the repository
```bash
git clone <repository-url>
cd web-based-ppc-app
```

2. Install dependencies
```bash
npm install
```

3. Start the development server
```bash
npm run dev
```

4. Open your browser to `http://localhost:3000`

### Usage

1. **Create a New Project**: Click "New Project" and complete the business intelligence questionnaire
2. **Select Service Package**: Choose between PPC Only, SEO Only, or PPC + SEO Combined
3. **Research Phases**: Navigate through the 5 research phases, copying prompts to Claude AI
4. **Save Responses**: Paste Claude AI responses back into the application
5. **Track Progress**: Monitor completion status and phase progression
6. **Auto-Analysis**: Once all phases are complete, project automatically transitions to "Completed" status
7. **View Analysis**: Access comprehensive analysis dashboard with insights, graphs, and strategic roadmap
8. **Implementation Planning**: Create detailed 12-month implementation plans with task management
9. **Export Reports**: Download detailed strategic analysis reports

## Project Structure

```
src/
├── app/                 # Next.js app directory
│   ├── page.tsx        # Dashboard
│   └── projects/       # Project management
├── components/         # Reusable UI components
├── lib/               # Utility libraries
│   ├── storage.ts     # Data persistence
│   └── prompt-generator.ts  # Claude prompt generation
└── types/             # TypeScript type definitions
```

## Data Models

### Project Structure
- **Business Intelligence**: Comprehensive business context and objectives
- **Claude Phases**: 5-phase research framework with prompts and responses
- **Project Assets**: Logos, documents, and supporting materials
- **Analysis**: Processed insights and strategic recommendations

### Phase Workflow
1. Review generated Claude AI prompt
2. Copy prompt to Claude AI interface
3. Paste response back into application
4. Mark phase as complete
5. Proceed to next phase

## Key Features

### Business Intelligence Collection
- Multi-step form with validation
- Industry-specific customization
- Competitor identification
- Goal and budget specification
- Success metrics definition

### Smart Prompt Engineering
- Context-aware prompt generation
- Industry-specific adaptations
- Progressive disclosure of information
- Comprehensive analysis requests

### Response Management
- Structured response storage
- Progress tracking
- Copy-to-clipboard functionality
- Auto-save capabilities

## Development

### Building for Production
```bash
npm run build
```

### Linting
```bash
npm run lint
```

### Type Checking
```bash
npm run type-check
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For support, please create an issue in the GitHub repository or contact the development team.

---

**Built with Claude AI strategic research methodology for professional PPC campaign development.**