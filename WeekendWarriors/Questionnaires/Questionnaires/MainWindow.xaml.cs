﻿using Questionnaires.QL.AST;
using Questionnaires.Renderer;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using Questionnaires.Types;
using System.Threading;
using Questionnaires.Renderer.Style;
using Questionnaires.QLS.AST;

namespace Questionnaires
{
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();            
        }

        private void Interpret_Click(object sender, RoutedEventArgs e)
        {
            Output.Text = "";

            var astFactory = new QL.AST.ASTFactory();
            var form = astFactory.CreateForm(InputQL.Text);
            var semanticAnalyzer = new SemanticAnalysis.SemanticAnalyzer();
            var analysisResult = semanticAnalyzer.AnalyzeForm(form);
            foreach (var analysisEvent in analysisResult.Events)
                Output.Text += analysisEvent.ToString() + '\n';

            var qlsFactory = new QLS.AST.ASTBuilder();
            if (InputQLS.Text != "")
            {
                var stylesheet = qlsFactory.Build(InputQLS.Text);
                var QuestionnaireBuilder = new QuestionnaireBuilder.QuestionnaireBuilder(form, stylesheet);
                QuestionnaireBuilder.Build();
            }
            else
            {
                var QuestionnaireBuilder = new QuestionnaireBuilder.QuestionnaireBuilder(form);
                QuestionnaireBuilder.Build();
            }
            
        }
    }
}
