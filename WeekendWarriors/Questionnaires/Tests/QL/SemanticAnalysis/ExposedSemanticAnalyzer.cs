﻿using Questionnaires.SemanticAnalysis;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Tests.QL.SemanticAnalysis
{
    /* Small helper class to expose the protected functions of the semantic alayzer that allow is to analyze nodes under the form. This has value for the
     * unit tests since we are unable to uniquely verify certain properties at the form level */
    public class ExposedSemanticAnalyzer : SemanticAnalyzer
    {
        public new Questionnaires.SemanticAnalysis.Result AnalyzeAstNode(Questionnaires.QL.AST.INode node)
        {
            return base.AnalyzeAstNode(node);
        }
    }
}
