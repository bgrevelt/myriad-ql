﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Questionnaires.Renderer.Containers
{
    public class Container
    {
        public string Name { get; set; }
        public List<Section> Sections { get; set; }
        public List<Questionnaires.QL.AST.Question> Questions { get; set; }
    }
}