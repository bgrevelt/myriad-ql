﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Questionnaires.SemanticAnalysis.SemenaticAnalysisEvents;
using System.Diagnostics;

namespace Questionnaires.AST
{
    public class QLString : IQLExpression
    {
        public QLString(string value)
        {
            this.Value = value;
        }

        public string Value
        {
            get;
        }

        public QLType? CheckOperandTypes(List<QLType> parameters, SemanticAnalysis.QLContext context, List<ISemenaticAnalysisEvent> events)
        {
            Trace.Assert(parameters.Count == 0);

            return QLType.String;
        }
    }
}